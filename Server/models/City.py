from pydantic import BaseModel, validator, constr


class City(BaseModel):
    id_country: int
    name_city: constr(max_length=32)
    additional_information: object = None

    @validator("name_city")
    def space_and_alph(cls, v: str):
        if " " not in v:
            return v.title()
        return ValueError("city name not contain spaces")


class CityGet(City):
    id: int

    class Config:
        orm_mode = True


class CityUpdate(CityGet):
    pass
