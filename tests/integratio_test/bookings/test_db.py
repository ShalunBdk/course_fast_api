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
    await db.bookings.add(booking_data)

    result = await db.bookings.get_one_or_none(user_id=user_id)

    booking_data = BookingPATCH(
        date_from=date(year=2024, month=8, day=1),
        date_to=date(year=2024, month=8, day=15),
    )

    await db.bookings.edit(booking_data, exclude_unset=True, id=result.id)

    await db.bookings.delete(id=result.id)

    await db.commit()