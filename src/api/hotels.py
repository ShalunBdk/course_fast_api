from datetime import date
from fastapi import Query, APIRouter, Body

from fastapi_cache.decorator import cache


from src.services.hotels import HotelService
from src.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException
from src.api.dependecies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение отелей")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Расположение отеля"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(examples="2024-10-05"),
    date_to: date = Query(examples="2024-10-06"),
):
    try:
        hotels = await HotelService(db).get_filtered_by_time(
            pagination,
            location,
            title,
            date_from,
            date_to,
        )
    except ObjectNotFoundException:
            raise HotelNotFoundHTTPException
    return {"status": "ok", "data": hotels}


@router.get("/{hotel_id}", summary="Получение отеля по ID")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException as e:
        raise HotelNotFoundHTTPException


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(
    hotel_id: int,
    db: DBDep,
):
    HotelService(db).delete_hotel(hotel_id)
    return {"status": "ok"}


@router.put("/{hotel_id}", summary="Обновление отеля")
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
):
    HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "ok"}


@router.patch("/{hotel_id}", summary="Частичное обновление отеля")
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
    db: DBDep,
):
    HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "ok"}


@router.post("/", summary="Создание отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель сочи 5 звезд у моря",
                    "location": "Сочи, ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель дубай у фонтана",
                    "location": "Дубай, ул. Абу, 511",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "ok", "data": hotel}
