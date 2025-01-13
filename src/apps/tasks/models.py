from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

# from src.apps.users.models import User

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
    # user: Mapped["User"] = relationship("User", init=False, back_populates="tasks")
    status: Mapped[EnumStatus]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    @property
    def user(self):

        return relationship("User", back_populates="tasks")
