from fastapi import APIRouter, Depends

from todo_list_pf.schemas import TaskSchema, TaskPublic
from todo_list_pf.database import get_session
from todo_list_pf.models import Task
from todo_list_pf.security import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session


router = APIRouter(prefix="/tasks", tags=["tasks"])

T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[Session, Depends(get_current_user)]


@router.post("/", response_model=TaskPublic)
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
