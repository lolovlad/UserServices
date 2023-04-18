from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import setting
from .table import base_table


connect = f'sqlite:///{setting.url_base}'
connect_async = f'sqlite+aiosqlite:///{setting.url_base}'

engine = create_engine(connect, echo=False)
engine_async = create_async_engine(connect_async, echo=False)

async_session = sessionmaker(bind=engine_async, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
