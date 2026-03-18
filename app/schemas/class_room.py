from uuid import UUID
from pydantic import BaseModel, Field
from typing import List


class CreateClass(BaseModel):
    name: str = Field(...)
    subject: str = Field(...)
    email: str = Field(...)


class UpdateClass(BaseModel):
    id: UUID = Field(...)
    name: str = Field(...)
    subject: str = Field(...)


class ResponseClass(BaseModel):
    id: UUID = Field(...)
    name: str = Field(...)
    subject: str = Field(...)
    teacher_id: UUID
    teacher_name: str = Field(...)
    teacher_email: str = Field(...)


class AddStudent(BaseModel):
    class_name: str = Field(...)
    emails: List[str] = Field(...)


class ReadStudent(BaseModel):
    class_name: str = Field(...)
