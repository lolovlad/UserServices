from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import setting
from .table import base_table


connect = f'postgresql+psycopg2://{setting.db_user}:{setting.db_pass}@{setting.db_host}:{setting.db_port}/{setting.db_name}'
connect_async = f'postgresql+asyncpg://{setting.db_user}:{setting.db_pass}@{setting.db_host}:{setting.db_port}/{setting.db_name}'

engine = create_engine(connect, echo=False)
engine_async = create_async_engine(connect_async, echo=False)

async_session = sessionmaker(bind=engine_async, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
