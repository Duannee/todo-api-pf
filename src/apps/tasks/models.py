from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, registry, relationship

register_metadata = registry()


class EnumStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    complete = "completed"


@register_metadata.mapped_as_dataclass
class Task:
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[EnumStatus]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    @declared_attr
    def user(cls):
        return relationship("User", back_populates="tasks")
