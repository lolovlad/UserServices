from ..database import get_session
from ..table import Country, City

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List


class GeolocationRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def add_city(self, city: City):
        try:
            self.__session.add(city)
            await self.__session.commit()
        except:
            await self.__session.rollback()

    async def add_country(self, country: Country):
        try:
            self.__session.add(country)
            await self.__session.commit()
        except:
            await self.__session.rollback()

    async def update_city(self, city: City):
        try:
            self.__session.add(city)
            await self.__session.commit()
        except:
            await self.__session.rollback()

    async def update_country(self, country: Country):
        try:
            self.__session.add(country)
            await self.__session.commit()
        except:
            await self.__session.rollback()

    async def get_city(self, id_city: int) -> City | None:
        return await self.__session.get(City, id_city)

    async def get_country(self, id_country: int) -> Country | None:
        return await self.__session.get(Country, id_country)

    async def get_all_list_city(self, id_country: int) -> List[City] | None:
        response = select(City).where(City.id_country == id_country)
        result = await self.__session.execute(response)
        return result.scalars().all()

    async def get_all_list_country(self) -> List[Country] | None:
        response = select(Country)
        result = await self.__session.execute(response)
        return result.scalars().all()

