# from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from backend.database import Base
# from datetime import datetime

# class TopUp(Base):
#     __tablename__ = "topups"

#     id = Column(Integer, primary_key=True, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     amount = Column(Float, nullable=False)
#     method = Column(String, nullable=False)  # e.g., 'bank_transfer', 'card'
#     status = Column(String, default="pending")  # e.g., 'pending', 'completed', 'failed'
#     date = Column(DateTime, default=datetime.utcnow)

#     owner = relationship("User", back_populates="topups")



from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from backend.database import Base  # adjust import based on your structure

class FundStatus(PyEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class TopUp(Base):
    __tablename__ = "topups"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String, nullable=False)

    # New fields
    status = Column(Enum(FundStatus), default=FundStatus.pending, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    processor_id = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    date = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="topups")
