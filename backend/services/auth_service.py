# backend/services/auth_service.py
import bcrypt
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import timedelta
from backend.config import settings
# import time date
from datetime import datetime

# Function to hash a password
def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')  # 👈 decode to string before storing



# Function to verify password against stored hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')  # 👈 convert back to bytes
    result = bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    return result



# JWT-related functions (already implemented in your Ticket 6)
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        print("Token expired.")
        return None
    except JWTError:
        print("Invalid token.")
        return None






