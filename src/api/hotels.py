from datetime import date
from fastapi import Query, APIRouter, Body

from src.api.dependecies import DBDep, PaginationDep
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH


router = APIRouter(prefix="/hotels",tags=["Отели"])


@router.get("/", summary="Получение отелей")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Расположение отеля"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2024-10-05"),
    date_to: date = Query(example="2024-10-06"),
):
    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     location = location,
    #     title = title,
    #     limit= per_page,
    #     offset= per_page * (pagination.page - 1)
    # )
    return await db.hotels.get_filtered_by_time(date_from=date_from, date_to=date_to)
    
@router.get("/{hotel_id}", summary="Получение отеля по ID")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    return await db.hotels.get_one_or_none(id = hotel_id)

@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(
    hotel_id: int,
    db: DBDep,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status":"ok"}

@router.put("/{hotel_id}", summary="Обновление отеля")
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status":"ok"}

@router.patch("/{hotel_id}", summary="Частичное обновление отеля")
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
    db: DBDep,
):
    await db.hotels.edit(hotel_data, exclude_unset=True,id=hotel_id)
    await db.commit()
    return {"status":"ok"}

@router.post("/", summary="Создание отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples={
    "1":{"summary":"Сочи", "value": {
        "title":"Отель сочи 5 звезд у моря",
        "location":"Сочи, ул. Моря, 1"
    }},
    "2":{"summary":"Дубай", "value": {
        "title":"Отель дубай у фонтана",
        "location":"Дубай, ул. Абу, 511"
    }}
    })
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status":"ok", "data":hotel}
