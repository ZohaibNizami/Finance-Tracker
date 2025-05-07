# Importing necessary libraries and dependencies
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from backend.dependencies import get_db, get_current_user
from backend.models.transaction import Transaction 
from backend.models.withdrawal import Withdrawal 
from backend.models.user import User  # Importing necessary models
from backend.schema.auth import  MessageResponse  # Import schemas for request and response
from backend.schema.withdrawal import WithdrawalCreate, WithdrawalResponse   # Import necessary schemas

# Create a new APIRouter instance for withdrawal routes
router = APIRouter(prefix="/withdraw")

# POST /withdraw: Initiates a withdrawal request
@router.post("/", response_model=MessageResponse)
async def initiate_withdrawal(
    withdraw_data: WithdrawalCreate,  # Withdrawal data (amount, method) sent by the user
    current_user: User = Depends(get_current_user),  # Get the current authenticated user
    db: Session = Depends(get_db)  # Database session
):
    """
    This endpoint processes a withdrawal request after checking if the user has enough balance.
    """
    # Step 1: Calculate the user's current balance (credit - debit)
    credits = db.query(Transaction).filter(Transaction.owner_id == current_user.id, Transaction.type == "credit").all()
    debits = db.query(Transaction).filter(Transaction.owner_id == current_user.id, Transaction.type == "debit").all()

    balance = sum([credit.amount for credit in credits]) - sum([debit.amount for debit in debits])

    # Step 2: Check if the user has enough balance for the withdrawal request
    if withdraw_data.amount > balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

    # Step 3: If balance is sufficient, create a new Withdrawal request (status = "pending")
    new_withdrawal = Withdrawal(
        owner_id=current_user.id,
        amount=withdraw_data.amount,
        method=withdraw_data.method,
        status="pending",  # Set status to "pending" until it's processed
        date=datetime.utcnow()
    )
    db.add(new_withdrawal)  # Add the new withdrawal record to the database
    db.commit()  # Commit the transaction
    db.refresh(new_withdrawal)  # Refresh to get updated data

    return {"message": "Withdrawal request submitted successfully."}  # Success message

# GET /withdraw/history: Fetches the user's withdrawal history
@router.get("/history", response_model=list[WithdrawalResponse])
async def get_withdrawal_history(
    db: Session = Depends(get_db),  # Database session
    current_user: User = Depends(get_current_user)  # Get the current authenticated user
):
    """
    Fetches and returns all withdrawal records of the authenticated user.
    """
    withdrawals = db.query(Withdrawal).filter(Withdrawal.owner_id == current_user.id).all()  # Fetch user's withdrawal history
    return withdrawals  # Return the list of withdrawals
