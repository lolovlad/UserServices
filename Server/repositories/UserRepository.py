from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session

from ..table import User, TypeUser

from ..models.User import *
from typing import List


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def get(self, id_user: int) -> GetUser:
        result = await self.__session.get(User, id_user)
        return GetUser.from_orm(result)

    async def get_by_login(self, login: str) -> User:
        response = select(User).where(User.login == login)
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def add(self, user: PostUser):
        try:
            user_table = User()
            user_dict = user.dict()
            for key in user.dict():
                if key != "password":
                    setattr(user_table, key, user_dict[key])
                else:
                    user_table.password = user_dict[key]
            self.__session.add(user_table)
            await self.__session.commit()
        except:
            await self.__session.rollback()