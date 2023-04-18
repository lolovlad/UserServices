from pydantic import BaseModel
from ..table import TypeUser


class BaseUser(BaseModel):
    name: str
    surname: str
    patronymic: str

    type_user: TypeUser

    login: str


class GetUser(BaseUser):
    id: int
    is_activ: bool

    class Config:
        orm_mode = True


class PostUser(BaseUser):
    password: str


class UserLogin(BaseModel):
    login: str
    password: str
