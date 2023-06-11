from pydantic import BaseModel, validator, constr, EmailStr
from pydantic.fields import ModelField
from email_validator import validate_email
from ..table import TypeUser
from .Role import RoleGet
from .Country import CountryGet
from .City import CityGet


class BaseUser(BaseModel):
    login: constr(max_length=50)

    name: constr(max_length=32)
    surname: constr(max_length=32)
    patronymic: constr(max_length=32)

    email: EmailStr
    phone: constr(max_length=24)

    additional_information: dict = {}

    @validator("login", "name", "surname", "patronymic")
    def space_and_alph(cls, v: str, field: ModelField):
        if " " not in v:
            if v.isalpha():
                return v
        raise ValueError(f"{field.name} not contain spaces or numbers")

    @validator("name", "surname", "patronymic")
    def title_filed(cls, v: str):
        return v.title()


class UserGet(BaseUser):
    id: int
    is_activ: bool
    role: RoleGet
    country: CountryGet
    city: CityGet

    class Config:
        orm_mode = True


class UserPost(BaseUser):
    password: str
    role_id: int
    country_id: int
    city_id: int
    additional_information: object = None

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    login: str
    password: str
