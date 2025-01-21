from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, registry


register_metadata = registry()


class EnumStatus(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    complete = "completed"


@register_metadata.mapped_as_dataclass
class User:
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    tasks: Mapped[List["Task"]] = relationship(
        default_factory=list, back_populates="user", cascade="all, delete-orphan"
    )


@register_metadata.mapped_as_dataclass
class Task:
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[EnumStatus]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(init=False, back_populates="tasks")

    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
