from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.apps.core.database import get_session
from src.apps.core.security import get_current_user
from src.apps.models import EnumStatus, Task
from src.apps.tasks.schemas import (
    TaskList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])

T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[Session, Depends(get_current_user)]


@router.post("/", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskSchema, session: T_Session, user: T_User):
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=user.id,
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/", response_model=TaskList)
def list_tasks(
    session: T_Session,
    user: T_User,
    status: EnumStatus | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    query = select(Task).where(Task.user_id == user.id)

    if status:
        query = query.filter(Task.status == status)

    tasks = session.scalars(query.offset(offset).limit(limit)).all()

    return {"tasks": tasks}


@router.get("/{task_id}", response_model=TaskPublic)
def get_task_id(task_id: int, session: T_Session, user: T_User):
    query = select(Task).where(Task.user_id == user.id, Task.id == task_id)
    task = session.scalars(query).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to you",
        )

    return task


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(task_id: int, task: TaskUpdate, session: T_Session, user: T_User):
    db_task = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    update_data = task.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    for key, value in update_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: T_Session, user: T_User):
    task = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    session.delete(task)
    session.commit()
