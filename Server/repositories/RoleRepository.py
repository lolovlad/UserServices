from fastapi import Depends

from ..table import Role
from ..database import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import List


class RoleRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def add_role(self, role: Role):
        try:
            self.__session.add(role)
            await self.__session.execute()
        except:
            await self.__session.rollback()

    async def get_role(self, id_role: int) -> Role | None:
        return await self.__session.get(Role, id_role)

    async def get_all_roles(self) -> List[Role] | None:
        response = select(Role).where().order_by(Role.id)
        result = await self.__session.execute(response)
        return result.scalars().all()

    async def update(self, role: Role):
        try:
            self.__session.add(role)
            await self.__session.execute()
        except:
            await self.__session.rollback()