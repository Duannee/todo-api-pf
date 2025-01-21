from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.apps.auth.schemas import Token
from src.apps.core.database import get_session
from src.apps.core.security import create_access_token, verify_password
from src.apps.models import User

router = APIRouter(prefix="/token", tags=["token"])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/", response_model=Token, status_code=status.HTTP_201_CREATED)
def login_for_access_token(
    session: T_Session,
    form_data: T_OAuth2Form,
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
