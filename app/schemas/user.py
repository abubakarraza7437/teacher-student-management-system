from enum import Enum
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    teacher = "teacher"
    student = "student"
    admin = "admin"


class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's name"
    )
    email: EmailStr = Field(
        ...,
        description="User's email"
    )
    password: str = Field(
        ...,
        min_length=6,
        description="User's password"
    )
    role: UserRole


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChangeUserPasswordRequest(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
