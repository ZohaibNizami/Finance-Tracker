from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.transaction import Transaction
from backend.models.user import User
from backend.schema.auth import MessageResponse
from backend.dependencies import get_current_user

trans_router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@trans_router.delete("/{transaction_id}", response_model=MessageResponse)
async def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"Attempting to delete transaction with ID: {transaction_id} for user ID: {current_user.id}")
    
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.owner_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    
    print(f"Transaction found: {transaction}")
    
    db.delete(transaction)
    db.commit()

    return MessageResponse(message="Transaction deleted successfully")
