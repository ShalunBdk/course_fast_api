from fastapi import APIRouter, Body

from src.services.bookings import BookingsService
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException, RoomNotFoundException, RoomNotFoundHTTPException
from src.schemas.bookings import BookingAddRequest
from src.api.dependecies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_all()


@router.get("/me", summary="Получить бронирования текущего пользователя")
async def get_my_bookings(
    user_id: UserIdDep,
    db: DBDep,
):
    return await BookingsService(db).get_filtered(user_id)


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
        booking = await BookingsService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "ok", "data": booking}
