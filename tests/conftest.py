# ruff: noqa: E402
import json
from typing import AsyncGenerator
import pytest

from httpx import AsyncClient
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.api.dependecies import get_db
from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAdd
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *  # noqa
from src.config import settings
from src.main import app
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_db():
    assert settings.DB_NAME == "test"


async def get_db_null_pull():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db()  -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pull():
        yield db


app.dependency_overrides[get_db] = get_db_null_pull


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_db):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    with open("tests/mock_hotels.json", encoding="utf-8") as file:
        hotels = json.load(file)
    with open("tests/mock_rooms.json", encoding="utf-8") as file:
        rooms = json.load(file)
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post("/auth/register", json={"email": "test@test.ru", "password": "1234"})


@pytest.fixture(scope="session")
async def authenticated_ac(ac, register_user):
    await ac.post("/auth/login", json={"email": "test@test.ru", "password": "1234"})
    assert ac.cookies["access_token"]
    yield ac
