from fastapi import Depends

from ..repositories.GeolocationRepository import GeolocationRepository
from ..table import City, Country
from ..models.City import City as CityModel, CityGet, CityUpdate
from ..models.Country import Country as CountryModel, CountryGet, CountryUpdate

from typing import List


class GeolocationServices:
    def __init__(self, repository: GeolocationRepository = Depends()):
        self.__repository: GeolocationRepository = repository

    async def add_city(self, city: CityModel):
        country = await self.__repository.get_country(city.id_country)
        if country is None:
            raise ValueError("country is empyti")

        city_entity = City(**city.dict())
        await self.__repository.add_city(city_entity)

    async def add_country(self, country: CountryModel):
        await self.__repository.add_country(Country(**country.dict()))

    async def get_city(self, id_city: int) -> CityGet:
        entity = await self.__repository.get_city(id_city)
        if entity is not None:
            return CityGet.from_orm(entity)
        raise ValueError("city not found")

    async def get_country(self, id_country: int) -> CountryGet:
        country = await self.__repository.get_country(id_country)
        if country is not None:
            return CountryGet.from_orm(country)
        raise ValueError("city not found")

    async def get_all_city(self, id_country: int) -> List[CityGet]:
        cities = await self.__repository.get_all_list_city(id_country)
        if cities is not None:
            return [CityGet.from_orm(entity) for entity in cities]
        raise ValueError("cities not found")

    async def get_all_country(self) -> List[CountryGet]:
        countries = await self.__repository.get_all_list_country()
        if countries is not None:
            return [CountryGet.from_orm(entity) for entity in countries]
        raise ValueError("countries not found")

    async def update_city(self, city: CityUpdate):
        country = await self.__repository.get_country(city.id_country)
        if country is None:
            raise ValueError("country is empyti")

        city_entity = City(**city.dict())
        await self.__repository.add_city(city_entity)

    async def update_country(self, country: CountryUpdate):
        await self.__repository.add_country(Country(**country.dict()))