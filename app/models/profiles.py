from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import UUID
from app.database import Base
from sqlalchemy import ForeignKey
from datetime import datetime, timezone


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

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    left_class_at: Mapped[datetime] = mapped_column(nullable=True)

    student = relationship(
        'User',
        backref='student_profile'
    )


class TeacherProfile(Base):
    __tablename__ = 'teacher_profile'

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    left_at: Mapped[datetime] = mapped_column(nullable=True)
    salary: Mapped[int] = mapped_column(
        nullable=True
    )
    teacher = relationship(
        'User',
        backref='teacher_profile'
    )
