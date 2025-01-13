from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from todo_list_pf.schemas import TaskSchema, TaskPublic, TaskList
from todo_list_pf.database import get_session
from todo_list_pf.models import Task
from todo_list_pf.security import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session
from todo_list_pf.models import EnumStatus


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
    query = select(Task).where(Task.id == task_id, Task.user_id == user.id)
    task = session.scalars(query).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to you",
        )

    return task
