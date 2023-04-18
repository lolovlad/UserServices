from Server.database import async_session
from Server.table import User, TypeUser

import asyncio


async def main():
    user = User(
                name="admin",
                surname="admin",
                patronymic="admin",
                is_activ=True,
                type_user=TypeUser.ADMIN,
                login="admin")
    user.password = "admin"
    async with async_session() as session:
        session.add(user)
        await session.commit()


asyncio.run(main())