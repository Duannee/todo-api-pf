from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from todo_list_pf.database import get_session
from http import HTTPStatus
from todo_list_pf.models import User
from sqlalchemy import select


from fastapi.security import OAuth2PasswordBearer
import pytz
from jwt import encode
from pwdlib import PasswordHash

from jwt import decode, DecodeError
from todo_list_pf.settings import Settings
from todo_list_pf.schemas import TokenData

settings = Settings()

pwd_context = PasswordHash.recommended()


def create_access_token(data: dict):
    to_encode = data.copy()

    utc_tz = pytz.utc

    expire_token = datetime.now(utc_tz) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire_token})

    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == token_data.username))

    if not user:
        raise credentials_exception
    return user
