from fastapi import APIRouter, Body, HTTPException

from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependecies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получить бронирования текущего пользователя")
async def get_my_bookings(
    user_id: UserIdDep,
    db: DBDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Создание бронирования")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Вип номер дубай",
                "value": {
                    "date_from": "2024-03-11",
                    "date_to": "2024-03-12",
                    "room_id": 8,
                },
            },
            "2": {
                "summary": "Простой номер сочи",
                "value": {
                    "date_from": "2024-11-01",
                    "date_to": "2024-11-03",
                    "room_id": 9,
                },
            },
        }
    ),
):
    try:
        _room_data = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    hotel: Hotel = await db.hotels.get_one(id=_room_data.hotel_id)
    room_price = _room_data.price
    _booking_data = BookingAdd(
        user_id=user_id, price=room_price, **booking_data.model_dump()
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as e:
        raise HTTPException(status_code=409, detail=e.detail)
    await db.commit()
    if booking:
        return {"status": "ok", "data": booking}
    else:
        return {"status": "not available"}
