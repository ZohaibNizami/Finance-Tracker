from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.transaction import Transaction
from backend.models.topups import TopUp      
from backend.models.withdrawal import Withdrawal 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    transactions = relationship("Transaction", back_populates="owner")
    topups = relationship("TopUp", back_populates="owner")
    withdrawals = relationship("Withdrawal", back_populates="owner")
    reset_tokens = relationship("PasswordResetToken", back_populates="user")


