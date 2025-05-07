from pydantic import BaseModel

# Balance Summary Schema
class BalanceSummaryResponse(BaseModel):
    current_balance: float
    total_topups: float
    total_withdrawals: float

# Dashboard Summary Schema (optional additional fields for dashboard)
class DashboardSummaryResponse(BaseModel):
    current_balance: float
    total_topups: float
    total_withdrawals: float
    # You can add more fields like monthly_spending, monthly_income, etc. here if needed.
