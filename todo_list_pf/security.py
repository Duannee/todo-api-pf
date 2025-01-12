from datetime import datetime, timedelta
import pytz

from jwt import encode
from pwdlib import PasswordHash


SECRET_KEY = "0b4b3c1e-0d1e-4f6f-8a7b-2e1f3d7e5c1d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = PasswordHash.recommended()


def create_access_token(data: dict):
    to_encode = data.copy()

    utc_tz = pytz.utc

    expire_token = datetime.now(utc_tz) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire_token})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
