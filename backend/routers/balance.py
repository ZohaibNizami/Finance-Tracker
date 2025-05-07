from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schema.dashboard import BalanceSummaryResponse
from backend.dependencies import get_db, get_current_user
from backend.models.user import User
from backend.models.topups import TopUp
from backend.models.withdrawal import Withdrawal
from backend.models.transaction import Transaction
from sqlalchemy import func

# Create APIRouter instance for /balances route
router = APIRouter()

# Endpoint for GET /balances
@router.get("/", response_model=BalanceSummaryResponse)
async def get_balance_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    total_topups = db.query(func.sum(TopUp.amount)).filter(TopUp.owner_id == current_user.id, TopUp.status == 'completed').scalar() or 0
    total_withdrawals = db.query(func.sum(Withdrawal.amount)).filter(Withdrawal.owner_id == current_user.id, Withdrawal.status == 'completed').scalar() or 0
    total_credits = db.query(func.sum(Transaction.amount)).filter(Transaction.owner_id == current_user.id, Transaction.type == 'credit').scalar() or 0
    total_debits = db.query(func.sum(Transaction.amount)).filter(Transaction.owner_id == current_user.id, Transaction.type == 'debit').scalar() or 0

    # Calculating current balance 
    current_balance = total_topups + total_credits - total_withdrawals - total_debits

    return BalanceSummaryResponse(
        current_balance=current_balance,
        total_topups=total_topups,
        total_withdrawals=total_withdrawals
    )
