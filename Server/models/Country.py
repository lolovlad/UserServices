from pydantic import BaseModel, validator, constr


class Country(BaseModel):
    name_country: str
    additional_information: object = None

    @validator("name_country")
    def space_and_alph(cls, v: str):
        if " " not in v:
            if v.isalpha():
                return v.title()
        raise ValueError("country name not contain spaces or numbers")


class CountryGet(Country):
    id: int

    class Config:
        orm_mode = True


class CountryUpdate(CountryGet):
    pass
