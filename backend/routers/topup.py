# Importing necessary libraries and dependencies
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from backend.dependencies import get_db, get_current_user
from backend.models.topups import TopUp  # Import TopUp model
from backend.models.user import User  # Import User model
from backend.schema.auth import MessageResponse 
from backend.schema.topup import TopUpCreate, TopUpResponse  # Import necessary schemas
 # Import necessary schemas

# Initialize the router for top-up related routes
router = APIRouter(prefix="/top-up")

# POST /top-up: This will initiate a top-up request
@router.post("/", response_model=MessageResponse)
async def initiate_topup(
    topup_data: TopUpCreate,  # The data for the top-up will be sent here
    current_user: User = Depends(get_current_user),  # Get the current user (authentication)
    db: Session = Depends(get_db)  # The database session
):
    """
    Initiates a top-up request. The status is set to "pending" initially.
    """
    new_topup = TopUp(
        owner_id=current_user.id,  # The authenticated user's ID
        amount=topup_data.amount,  # The amount for top-up
        method=topup_data.method,  # The method of top-up (e.g., credit card, PayPal)
        status="pending",  # Initially, the top-up status is set to pending
        date=datetime.utcnow()  # The current date and time when the top-up is requested
    )
    db.add(new_topup)  # Add the new top-up to the session
    db.commit()  # Commit the transaction to the database
    db.refresh(new_topup)  # Refresh the top-up to get the updated data

    return {"message": "Top-up request initiated successfully."}  # Return success message

# GET /top-up/history: This will return the history of top-ups for the authenticated user
@router.get("/history", response_model=list[TopUpResponse])
async def get_topup_history(
    db: Session = Depends(get_db),  # The database session
    current_user: User = Depends(get_current_user)  # Get the current user (authentication)
):
    """
    Fetches and returns the user's top-up history.
    """
    topups = db.query(TopUp).filter(TopUp.owner_id == current_user.id).all()  # Fetch all top-ups for the current user
    return topups  # Return the list of top-ups as a response


