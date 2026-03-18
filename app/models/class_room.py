from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.user import User

# Many-to-many association table: class <-> student
class_students = Table(
    "class_students",
    Base.metadata,
    Column(
        "class_id",
        ForeignKey("class.id"),
        primary_key=True,
    ),
    Column(
        "student_id",
        ForeignKey("user.id"),
        primary_key=True,
    ),
)


class Class(Base):
    __tablename__ = "class"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    subject: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    teacher_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
    )
    teacher: Mapped[User] = relationship(
        "User",
        foreign_keys=[teacher_id],
    )

    students: Mapped[List[User]] = relationship(
        "User",
        secondary=class_students,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
    )
