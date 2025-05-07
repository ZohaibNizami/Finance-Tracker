
from fastapi import APIRouter
from backend.schema.currency import CurrencyRatesResponse
from backend.services.currency_service import get_live_currency_rates


currency_router = APIRouter()

@currency_router.get("/currency-rates", response_model=CurrencyRatesResponse)
def get_rates():
    return get_live_currency_rates()



