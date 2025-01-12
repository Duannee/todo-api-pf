from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublicSchema(BaseModel):
    id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str
