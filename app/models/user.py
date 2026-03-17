from datetime import datetime, timezone
from uuid import uuid4, UUID

from sqlalchemy import Enum
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("teacher", "student", "admin", name="user_role"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )