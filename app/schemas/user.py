from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID


class UserCreate(BaseModel):
    name: str = Field(...,
                      min_length=2,
                      max_length=100,
                      description="User's name"
                      )
    email: EmailStr = Field(..., description="User's email")
    password: str
    role: str

    @validator('role')
    def role_validator(cls, v):
        if v not in ['teacher', 'student', 'admin']:
            raise ValueError('role must be one of teacher, student, or admin')
        return v

    class Config:
        from_attributes = True


class UserRead(UserCreate):
    id: UUID
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
