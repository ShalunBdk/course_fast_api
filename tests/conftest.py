import json
import pytest

from httpx import AsyncClient
from sqlalchemy import insert

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

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_db):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    with open('tests/mock_hotels.json', encoding="utf-8") as file:
        data_hotels = json.load(file)
    with open('tests/mock_rooms.json', encoding="utf-8") as file:
        data_rooms = json.load(file)
    insert_hotels_stmt = insert(HotelsOrm).values(data_hotels)
    insert_rooms_stmt = insert(RoomsOrm).values(data_rooms)
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.session.execute(insert_hotels_stmt)
        await db.session.execute(insert_rooms_stmt)
        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "test@test.ru",
                "password": "1234"
            }
        )