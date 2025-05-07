from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from backend.health import router as health_router
from backend.routers.auth import router as auth_router 
from backend.config import settings
from pyngrok import ngrok 
import asyncio
from contextlib import asynccontextmanager
import logging
from backend.routers.topup import router as topup_router
from backend.routers.withdraw import router as withdraw_router 
from backend.routers.balance import router as balances_router
from backend.routers.dashboard import router as dashboard_router
from backend.routers.user import put_router  # Make sure this import exists
from backend.routers.transaction import trans_router
from backend.routers.internal import internel_router
from backend.routers.currency  import currency_router
from starlette.responses import JSONResponse


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
APPLICATION_PORT = 8000
ngrok_url = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ngrok_url
    tunnel = None

    if settings.NGROK_AUTH_TOKEN:
        try:
            logger.info("Setting up ngrok tunnel...")
            ngrok.set_auth_token(settings.NGROK_AUTH_TOKEN)
            tunnel = await asyncio.to_thread(ngrok.connect, APPLICATION_PORT, proto="http")
            ngrok_url = tunnel.public_url
            logger.info(f"ngrok tunnel started: {ngrok_url}")
        except Exception as e:
            logger.error(f"Error setting up ngrok tunnel: {str(e)}")
    else:
        logger.warning("NGROK_AUTH_TOKEN not set — skipping ngrok setup.")

    yield

    if tunnel:
        try:
            logger.info("Tearing down ngrok tunnel...")
            await asyncio.to_thread(ngrok.disconnect, tunnel.public_url)
        except Exception as e:
            logger.error(f"Error disconnecting ngrok tunnel: {str(e)}")

# ✅ Register lifespan
app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(router=health_router)
app.include_router(auth_router, prefix="/auth" )
app.include_router(topup_router)
app.include_router(withdraw_router)
app.include_router(balances_router, prefix="/balances")
app.include_router(dashboard_router) 
app.include_router(put_router)
app.include_router(trans_router)
app.include_router(internel_router)
app.include_router(currency_router)
# NOTE: Internal routes should be secured via token-based auth or IP restriction in production.


# CORS config
origins = [
    settings.FRONTEND_ORIGIN,
    "http://localhost:3000",
   "https://saving-close-goat.ngrok-free.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Optional: Generic handler for unexpected errors
@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    import traceback
    logger.error(f"Unhandled exception: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."}
    )




