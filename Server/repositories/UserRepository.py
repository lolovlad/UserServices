from fastapi import Depends

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session

from ..table import User, TypeUser

from ..models.User import *
from typing import List


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def get_count_users(self) -> int:
        response = select(func.count(User.id))
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def get_users_by_role_offset(self, start: int, end: int, role_user: int) -> List[User] | None:
        if role_user == 0:
            response = select(User)
        else:
            response = select(User).where(User.role_id == role_user)
        response = response.offset(start).fetch(end).order_by(User.id)
        result = await self.__session.execute(response)
        return result.scalars().all()

    async def get(self, id_user: int) -> User | None:
        result = await self.__session.get(User, id_user)
        return result

    async def get_by_login(self, login: str) -> User:
        response = select(User).where(User.login == login)
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def add(self, user: UserPost):
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