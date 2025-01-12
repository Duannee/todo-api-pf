from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import registry, Mapped, mapped_column
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

register_metadata = registry()


class EnumStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@register_metadata.mapped_as_dataclass
class User:
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now(), nullable=False
    )


@register_metadata.mapped_as_dataclass
class Task:
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[EnumStatus] = mapped_column(
        SQLAlchemyEnum(EnumStatus), nullable=False, default=EnumStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now(), nullable=False
    )
