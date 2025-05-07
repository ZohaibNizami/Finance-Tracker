from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.dependencies import get_db
from backend.models.topups import TopUp
from backend.models.withdrawal import Withdrawal
from backend.models.transaction import Transaction
from backend.schema import FundStatusUpdateInternal
from backend.schema.auth import MessageResponse

internel_router = APIRouter(prefix="/internal")

@internel_router.post("/update-fund-status", response_model=MessageResponse)
async def update_fund_status(update_data: FundStatusUpdateInternal, db: Session = Depends(get_db)):
    record_type = update_data.record_type.lower()
    record_id = update_data.record_id

    # Fetch record based on type
    if record_type == "topup":
        record = db.query(TopUp).filter(TopUp.id == record_id).first()
    elif record_type == "withdrawal":
        record = db.query(Withdrawal).filter(Withdrawal.id == record_id).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid record_type. Must be 'topup' or 'withdrawal'.")

    if not record:
        raise HTTPException(status_code=404, detail="Record not found.")

    if record.status in ("completed", "failed"):
        raise HTTPException(status_code=400, detail=f"Record already in final state: {record.status}")

    # Save previous status
    previous_status = record.status

    # Update status and metadata
    record.status = update_data.new_status
    record.processed_at = update_data.processed_at or datetime.utcnow()
    record.processor_id = update_data.processor_id
    record.error_message = update_data.error_message

    # Handle transaction creation if transitioning to 'completed'
    if update_data.new_status == "completed" and previous_status != "completed":
        transaction = Transaction(
            owner_id=record.owner_id if record_type == "topup" else record.user_id,
            type="credit" if record_type == "topup" else "debit",
            amount=record.amount,
            description=f"{record_type.capitalize()} transaction",
            date=datetime.utcnow()
        )
        db.add(transaction)

    db.commit()
    return {"message": f"{record_type.capitalize()} status updated successfully."}
