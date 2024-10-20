import pytest

from tests.conftest import get_db_null_pull


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-01-12", "2024-01-13", 200),
        (1, "2024-01-12", "2024-01-13", 200),
        (1, "2024-01-12", "2024-01-13", 200),
        (1, "2024-01-12", "2024-01-13", 200),
        (1, "2024-01-12", "2024-01-13", 200),
        (1, "2024-01-12", "2024-01-13", 409),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pull():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booking_count",
    [
        (1, "2024-01-12", "2024-01-13", 1),
        (1, "2024-01-12", "2024-01-13", 2),
        (1, "2024-01-12", "2024-01-13", 3),
    ],
)
async def test_add_booking_get_my_bookings(
    delete_all_bookings, room_id, date_from, date_to, booking_count, authenticated_ac
):
    booking_response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert booking_response.status_code == 200
    me_response = await authenticated_ac.get("/bookings/me")
    assert me_response.status_code == 200
    assert len(me_response.json()) == booking_count
