from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo_list_pf.database import get_session
from todo_list_pf.models import User
from todo_list_pf.schemas import UserPublicSchema, UserSchema
from todo_list_pf.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

T_Session = Annotated[Session, Depends(get_session)]


@router.post("/", response_model=UserPublicSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
