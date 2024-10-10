from datetime import date
from src.schemas.bookings import BookingAdd, BookingPATCH


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=13),
        room_id=user_id,
        user_id=room_id,
        price=100,
    )
    booking = await db.bookings.add(booking_data)

    result = await db.bookings.get_one_or_none(id=booking.id)
    assert result
    assert booking.id == result.id
    assert booking.room_id == result.room_id

    update_booking_data = BookingPATCH(
        date_from=date(year=2024, month=8, day=1),
        date_to=date(year=2024, month=8, day=15),
        price=10000
    )
    await db.bookings.edit(update_booking_data, exclude_unset=True, id=result.id)
    updated_booking = await db.bookings.get_one_or_none(id=result.id)
    assert updated_booking
    assert result.id == updated_booking.id
    assert updated_booking.date_from == date(year=2024, month=8, day=1)

    await db.bookings.delete(id=result.id)
    booking = await db.bookings.get_one_or_none(id=result.id)
    assert not booking