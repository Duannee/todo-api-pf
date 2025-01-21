from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.apps.models import EnumStatus


class TaskSchema(BaseModel):
    title: str
    description: str
    status: EnumStatus


class TaskPublic(TaskSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskList(BaseModel):
    tasks: list[TaskPublic]


class TaskUpdate(BaseModel):
    title: Optional[str] | None = None
    description: Optional[str] | None = None
    state: Optional[EnumStatus] | None = None
