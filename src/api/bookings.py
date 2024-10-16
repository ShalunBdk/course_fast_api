from datetime import date
from fastapi import Query, APIRouter, Body

from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependecies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings",tags=["Бронирование"])


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()

@router.get("/me", summary="Получить бронирования текущего пользователя")
async def get_my_bookings(
    user_id: UserIdDep,
    db: DBDep,
):
    return await db.bookings.get_filtered(user_id = user_id)

@router.post("", summary="Создание бронирования")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(openapi_examples={
    "1":{"summary":"Вип номер дубай", "value": {
        "date_from":"2024-03-11",
        "date_to":"2024-03-12",
        "room_id": 8

    }},
    "2":{"summary":"Простой номер сочи", "value": {
        "date_from":"2024-11-01",
        "date_to":"2024-11-03",
        "room_id": 9
    }}
    })
):
    _room_data = await db.rooms.get_one_or_none(id = booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=_room_data.hotel_id)
    room_price = _room_data.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    if booking:
        return {"status":"ok", "data":booking}
    else:
        return {"status":"not available"}