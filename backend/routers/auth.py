from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schema.auth import RegisterRequest, MessageResponse
from backend.models.user import User
from backend.services.auth_service import hash_password
from backend.services.auth_service import create_access_token  , verify_password
from backend.schema.auth import LoginRequest, TokenResponse
from backend.dependencies import get_current_user
from fastapi.security import OAuth2PasswordBearer
from backend.schema.auth import UserResponse
from backend.schema.auth import TransactionResponse
from backend.models.transaction import Transaction
from datetime import datetime
from backend.schema.auth import TransactionCreate
from backend.schema.auth import MessageResponse 
from backend.models.user import User
from backend.models.topups import TopUp
from backend.schema.topup import TopUpCreate, TopUpResponse
from backend.schema.auth import MessageResponse 
from backend.models.PasswordResetToken import PasswordResetToken
from backend.schema.auth import ResetPasswordConfirm
from backend.schema.auth import ResetPasswordRequest
import uuid
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/register", response_model=MessageResponse)
def register_user(user_data: RegisterRequest, db: Session = Depends(get_db)):
   
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pwd = hash_password(user_data.password)

    
    new_user = User(
        email=user_data.email,
        name=user_data.name,  
        phone_number=user_data.phoneNumber,  
        hashed_password=hashed_pwd  
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return MessageResponse(message="User registered successfully.")


from fastapi import Form

@router.post("/token", response_model=TokenResponse)
def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token_data = {"sub": user.email, "user_id": user.id}
    access_token = create_access_token(data=token_data)
    return TokenResponse(access_token=access_token, token_type="bearer")



@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return {"email": current_user.email, "name": current_user.name}



@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[TransactionResponse])
async def get_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).filter(Transaction.owner_id == current_user.id).all()
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_by_id(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.owner_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction


@router.post("/transactions", response_model=MessageResponse)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_transaction = Transaction(
        type=transaction_data.type,
        amount=transaction_data.amount,
        description=transaction_data.description,
        date=datetime.utcnow(),           # 👈 current time
        owner_id=current_user.id          # 👈 authenticated user ID
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {"message": "Transaction created successfully"}



@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    reset_token = PasswordResetToken(
        token=uuid.uuid4().hex,
        user_id=user.id,
        email=user.email,  # <-- add this
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )

    db.add(reset_token)
    db.commit()
    print(f"Reset token created: {reset_token.token}")
    return {"message": "Reset token generated", "token": reset_token.token}



    
@router.post("/reset-password-confirm")
async def reset_password_confirm(reset_data: ResetPasswordConfirm, db: Session = Depends(get_db)):
    token_entry = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token == reset_data.token,
            PasswordResetToken.email == reset_data.email,
            PasswordResetToken.expires_at > datetime.utcnow()
        )
        .first()
    )

    if not token_entry:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # 2. Find associated user
    user = db.query(User).filter(User.id == token_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Hash and update password
    user.hashed_password = hash_password(reset_data.new_password)

    # 4. Invalidate/delete token
    db.delete(token_entry)
    db.commit()

    return {"message": "Password reset successfully"}


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Logout successful"}









