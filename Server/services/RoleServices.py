from fastapi import Depends
from ..table import Role
from ..repositories.RoleRepository import RoleRepository
from ..models.Role import Role, RoleGet

from typing import List


class RoleServices:
    def __init__(self, repository: RoleRepository = Depends()):
        self.__repository: RoleRepository = repository

    async def add_role(self, role: Role):
        role = Role(**role.dict())
        await self.__repository.add_role(role)

    async def get_role(self, id_role: int) -> RoleGet:
        role = await self.__repository.get_role(id_role)
        if role is not None:
            return RoleGet.from_orm(role)
        raise ValueError("role is none")

    async def get_all_role(self) -> List[RoleGet]:
        roles = await self.__repository.get_all_roles()
        if roles is not None:
            return [RoleGet.from_orm(entity) for entity in roles]
        raise ValueError("role is none")