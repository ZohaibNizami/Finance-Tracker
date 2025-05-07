from pydantic import BaseModel, EmailStr, Field , field_validator , validator
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Annotated

class RegisterRequest(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
    confirmPassword: Annotated[str, Field(min_length=8)]
    name: Annotated[str, Field(min_length=2, max_length=50)]
    phoneNumber: Annotated[str, Field(pattern=r'^\+?\d{10,15}$')]

    @field_validator("confirmPassword")
    def passwords_match(cls, value, values):
        if "password" in values.data and value != values.data["password"]:
            raise ValueError("Passwords do not match")
        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class MessageResponse(BaseModel):
    message: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    type: str
    amount: float
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    date: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class ResetPasswordConfirm(BaseModel):
    token: str
    email: EmailStr
    new_password: str = Field(min_length=8, description="New password must be at least 8 characters")
    @validator('new_password')
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class Userschema(BaseModel):
    id: int
    name: str  # adjust field names based on your actual SQLAlchemy model
    email: str

    class Config:
        orm_mode = True

class transactionAmount(BaseModel):
    owner_id: int
    name: str

    class Config:
        orm_mode = True