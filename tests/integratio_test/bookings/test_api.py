import pytest

from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-01-12", "2024-01-13", 200),
    (1, "2024-01-12", "2024-01-13", 200),
    (1, "2024-01-12", "2024-01-13", 200),
    (1, "2024-01-12", "2024-01-13", 200),
    (1, "2024-01-12", "2024-01-13", 200),
    (1, "2024-01-12", "2024-01-13", 500),
])
async def test_add_booking(
    room_id, date_from, date_to, status_code,
    authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"
        assert "data" in res

@pytest.fixture(scope="session")
async def delete_all_bookings(setup_database):
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.bookings.delete()
        await db_.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, status_code, booking_count", [
    (1, "2024-01-12", "2024-01-13", 200, 1),
    (1, "2024-01-12", "2024-01-13", 200, 2),
    (1, "2024-01-12", "2024-01-13", 200, 3)
])
async def test_add_booking_get_my_bookings(delete_all_bookings,
    room_id, date_from, date_to, status_code, booking_count,
    authenticated_ac                                           
):
    booking_response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    me_response = await authenticated_ac.get(
        "/bookings/me"
    )
    assert booking_response.status_code == status_code
    assert me_response.status_code == status_code
    res = me_response.json()
    assert len(res) == booking_count