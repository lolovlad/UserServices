from fastapi import Depends
from ..models.User import *
from ..repositories import UserRepository
from typing import List


class UserServices:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repo: UserRepository = user_repository
        self.__count_user_in_page: int = 20

    @property
    def count_user_in_page(self):
        return self.__count_user_in_page

    async def get_count_page(self) -> int:
        count_users = await self.__user_repo.get_count_users()
        is_dop_page = 1 if count_users % self.__count_user_in_page > 0 else 0
        return count_users // self.__count_user_in_page + is_dop_page

    async def get_list_user_page(self, num_page: int, role_user: int) -> List[UserGet]:
        start_position = self.__count_user_in_page * (num_page - 1)
        end_position = self.__count_user_in_page * num_page
        users_entity = await self.__user_repo.get_users_by_role_offset(start_position, end_position, role_user)
        user = [UserGet.from_orm(entity) for entity in users_entity]
        return user

    async def get_user(self, id_user: int) -> UserGet:
        user = await self.__user_repo.get(id_user)
        return user

    async def add_user(self, user: UserPost):
        await self.__user_repo.add(user)
