from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter")
    return password


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase, UserLogin):
    @field_validator("password")
    @classmethod
    def validate_user_password(cls, v):
        return validate_password(v)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    disabled: Optional[bool] = None

    @field_validator("password")
    @classmethod
    def validate_update_password(cls, v):
        if v is not None:  # Only validate if password is provided
            return validate_password(v)
        return v


class User(UserBase):
    id: UUID
    disabled: bool
    email: EmailStr

    class Config:
        from_attributes = True


class UserInDB(UserCreate):
    hashed_password: str


class TokenData(BaseModel):
    email: str | None = None
