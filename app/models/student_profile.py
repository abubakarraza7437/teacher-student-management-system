from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import UUID
from app.database import Base
from sqlalchemy import ForeignKey
from datetime import datetime, timezone


class Student(Base):
    __tablename__ = "student"


class StudentProfile(Base):
    __tablename__ = 'student_profile'

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
    )
    roll_number: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        nullable=False
    )
    dues: Mapped[int] = mapped_column(
        autoincrement=False,
        nullable=True
    )
    pending_dues: Mapped[int] = mapped_column(
        autoincrement=False,
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )
    classes: Mapped[int] = mapped_column(
        ForeignKey("class.id"),
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    left_class_at: Mapped[datetime] = mapped_column(nullable=True)

    student = relationship(
        'User',
        backref='student_profile'
    )
    student_classes = relationship(
        'class',
        backref='student_profile'
    )
