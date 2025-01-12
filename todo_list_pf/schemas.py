from pydantic import BaseModel, EmailStr
from todo_list_pf.models import EnumStatus


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


class TodoSchema(BaseModel):
    title: str
    description: str
    status: EnumStatus


class TodoPublicSchema(TodoSchema):
    id: int
