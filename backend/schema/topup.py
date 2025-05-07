from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class FundStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class TopUpBase(BaseModel):
    amount: float
    method: str

class TopUpCreate(TopUpBase):
    pass

class TopUpResponse(TopUpBase):
    id: int
    owner_id: int
    status: FundStatus
    processed_at: Optional[datetime]
    processor_id: Optional[str]
    error_message: Optional[str]
    date: datetime

    class Config:
        orm_mode = True
