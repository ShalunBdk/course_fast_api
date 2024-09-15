from fastapi import Query, APIRouter, Body

from sqlalchemy import func, insert, select

from repositories.hotels import HotelsRepository
from src.api.dependecies import PaginationDep
from src.models.hotels import HotelsOrm
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelPATCH


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

@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status":"ok"}

@router.patch("/{hotel_id}", summary="Частичное обновление отеля")
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status":"ok"}

@router.put("/{hotel_id}", summary="Обновление отеля")
def put_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status":"ok"}

@router.post("/", summary="Создание отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
        hotel = await HotelsRepository(session).add(**hotel_data.model_dump())
        await session.commit()

    return {"status":"ok", "data":hotel}
