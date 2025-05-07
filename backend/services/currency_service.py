import requests
from cachetools import TTLCache
from backend.config import settings

# Cache: max 1 item, expires after 15 minutes
currency_cache = TTLCache(maxsize=1, ttl=settings.CACHE_TTL_MINUTES * 60)

def get_live_currency_rates():
    cache_key = "currency_rates"

    if cache_key in currency_cache:
        return currency_cache[cache_key]

    try:
        response = requests.get(
            settings.EXCHANGE_API_BASE_URL,
            params={"base": "USD", "symbols": "USD,EUR,PKR,GBP"}
        )
        print("Raw response:", response.text)  # 🔥 DEBUG LINE
        data = response.json()

        if "rates" in data:
            rates = {
                "USD": data["rates"].get("USD", 0.0),
                "EUR": data["rates"].get("EUR", 0.0),
                "PKR": data["rates"].get("PKR", 0.0),
                "GBP": data["rates"].get("GBP", 0.0),
            }

            currency_cache[cache_key] = rates
            return rates

    except Exception as e:
        print("Currency API error:", e)

    return {"USD": 0.0, "EUR": 0.0, "PKR": 0.0, "GBP": 0.0}
