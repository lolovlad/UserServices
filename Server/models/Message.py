from pydantic import BaseModel
from ..table import TypeUser


class Message(BaseModel):
    content: str


class Token(BaseModel):
    access_token: str
    refresh_token: str = ""
    token_type: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str = ""
    token_type: str
    type_user: TypeUser
