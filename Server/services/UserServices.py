from fastapi import Depends
from ..models.User import *
from ..repositories import UserRepository


class UserServices:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repo: UserRepository = user_repository

    async def get_user(self, id_user: int) -> GetUser:
        user = await self.__user_repo.get(id_user)
        return user

    async def add_user(self, user: PostUser):
        await self.__user_repo.add(user)
