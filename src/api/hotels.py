from fastapi import Query, APIRouter, Body

from repositories.hotels import HotelsRepository
from src.api.dependecies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH


router = APIRouter(prefix="/hotels",tags=["Отели"])


@router.get("/", summary="Получение отелей")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description="Расположение отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location = location,
            title = title,
            limit= per_page,
            offset= per_page * (pagination.page - 1)
        )
    
@router.get("/{hotel_id}", summary="Получение отеля по ID")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id = hotel_id)

@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status":"ok"}

@router.put("/{hotel_id}", summary="Обновление отеля")
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd

):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status":"ok"}

@router.patch("/{hotel_id}", summary="Частичное обновление отеля")
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True,id=hotel_id)
        await session.commit()
    return {"status":"ok"}

@router.post("/", summary="Создание отеля")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status":"ok", "data":hotel}
