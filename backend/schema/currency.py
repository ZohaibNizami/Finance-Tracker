from pydantic import BaseModel
from typing import Optional

class CurrencyRatesResponse(BaseModel):
    USD: float
    EUR: float
    PKR: float
    GBP: float
