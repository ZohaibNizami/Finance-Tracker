# # backend/config.py


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FRONTEND_ORIGIN: str = "https://v0-fastapi-frontend-in-next-js.vercel.app/"
    NGROK_AUTH_TOKEN: str  # ✅ correct line
    ENABLE_NGROK: bool = False

    EXCHANGE_API_KEY: str
    EXCHANGE_API_BASE_URL: str = "http://data.fixer.io/api/latest"
    CACHE_TTL_MINUTES: int = 15 
    # backend/config.py

 # 15 minutes

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()


EXCHANGE_API_BASE_URL: str = "https://api.exchangerate.host/latest"
