from pydantic import BaseModel, ValidationError, validator, constr


class Role(BaseModel):
    name_role: constr(min_length=3, max_length=12)

    @validator('name_role')
    def space_and_alph(cls, v: str):
        if " " not in v:
            if v.isalpha():
                return v
        raise ValueError("role name not contain spaces or numbers")


class RoleGet(Role):
    id: int

    class Config:
        orm_mode = True