import asyncio

import pytest

from fastapi.testclient import TestClient
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from Server.settings import setting
from Server.table import base_table

from Server.app import app
from Server.database import get_session

connect_async = f'postgresql+asyncpg://{setting.db_name_test}:{setting.db_pass_test}@{setting.db_host_test}:{setting.db_port_test}/{setting.db_name_test}'

engine_async_test = create_async_engine(connect_async, echo=False)
async_session_test = sessionmaker(bind=engine_async_test, class_=AsyncSession, expire_on_commit=False)

base_table.metadata.bind = engine_async_test


async def override_get_session() -> AsyncSession:
    async with async_session_test() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True, scope="session")
async def pre_database():
    async with engine_async_test.begin() as conn:
        await conn.run_sync(base_table.metadata.create_all)
    yield
    async with engine_async_test.begin() as conn:
        await conn.run_sync(base_table.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
def get_token():
    payload = f"grant_type=&username=vlad&password=vlad&client_id=&client_secret="
    response = client.post("/v1/login/sign-in/", json=payload, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    })
    token = response.json()['access_token']
    return f'Bearer {token}'


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
