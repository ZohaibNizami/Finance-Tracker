from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base 

import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  
    amount = Column(Float)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="transactions")

