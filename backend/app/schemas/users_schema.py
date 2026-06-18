from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    date_of_birth: date
    subscription_type: Literal["premium"] | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    surname: str
    date_of_birth: date
    subscription_type: str
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserEdit(BaseModel):
    name: str
    surname: str
    date_of_birth: date
    subscription_type: Literal["premium", "standard"]


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
