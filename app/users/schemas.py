import hashlib
import re
from typing_extensions import Annotated

from typing import Optional
from pydantic import BaseModel, BeforeValidator, EmailStr


def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter")
    return password


def validate_email(email: str) -> str:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email address")
    return email

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    disabled: bool

    class Config:
        from_attributes = True

class UserInDB(UserCreate):
    hashed_password: str

class TokenData(BaseModel):
    email: str | None = None