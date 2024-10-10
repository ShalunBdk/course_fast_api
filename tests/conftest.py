import json
import pytest

from httpx import AsyncClient
from sqlalchemy import insert

from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAdd
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.config import settings
from src.main import app
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.utils.db_manager import DBManager

@pytest.fixture(scope="session", autouse=True)
async def check_test_db():
    assert settings.DB_NAME == "test"

@pytest.fixture(scope="function")
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_db):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    with open('tests/mock_hotels.json', encoding="utf-8") as file:
        hotels = json.load(file)
    with open('tests/mock_rooms.json', encoding="utf-8") as file:
        rooms = json.load(file)
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "test@test.ru",
            "password": "1234"
        }
    )