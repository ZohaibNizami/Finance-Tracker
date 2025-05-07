from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class FundStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class FundStatusUpdateInternal(BaseModel):
    record_id: int
    record_type: str  # "topup" or "withdrawal"
    new_status: FundStatus
    processor_id: Optional[str] = None
    error_message: Optional[str] = None
    processed_at: Optional[datetime] = None
