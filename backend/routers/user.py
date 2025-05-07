from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.models import User
from backend.schema.auth import UserUpdate, UserResponse
from backend.dependencies import get_current_user, get_db

put_router = APIRouter(prefix="/users", tags=["Users"])

@put_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure only the owner can update
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user.")

    # Get fresh user record from DB
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Check email uniqueness if email is being updated
    if update_data.email and update_data.email != db_user.email:
        existing_user = db.query(User).filter(User.email == update_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use.")

    # Apply updates if values are provided
    if update_data.name is not None:
        db_user.name = update_data.name
    if update_data.email is not None:
        db_user.email = update_data.email

    db.commit()
    db.refresh(db_user)

    return db_user
