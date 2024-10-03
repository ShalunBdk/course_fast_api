from datetime import date
from fastapi import Query, APIRouter, Body

from schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependecies import DBDep, PaginationDep, UserIdDep

router = APIRouter(prefix="/bookings",tags=["Бронирование"])


@router.post("/", summary="Создание бронирования")
async def create_room(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(openapi_examples={
    "1":{"summary":"Вип номер дубай", "value": {
        "date_from":"2025-03-11",
        "date_to":"2025-03-12",
        "room_id": 8

    }},
    "2":{"summary":"Простой номер сочи", "value": {
        "date_from":"2024-11-01",
        "date_to":"2024-11-03",
        "room_id": 9
    }}
    })
):
    _room_data = await db.rooms.get_filtered(id = booking_data.room_id)
    _booking_data = BookingAdd(user_id=user_id, price=_room_data[0].price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status":"ok", "data":booking}