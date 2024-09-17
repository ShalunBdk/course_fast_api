from fastapi import APIRouter, Body, Query

from repositories.rooms import RoomsRepository
from schemas.rooms import RoomAdd, RoomPATCH
from src.database import async_session_maker 


router = APIRouter(prefix="/hotels",tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение номеров")
async def get_rooms(
    hotel_id: int,
    title: str | None = Query(None, description="Название номера"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id = hotel_id,
            title = title,
        )

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по ID")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id = room_id)

@router.post("/{hotel_id}/rooms", summary="Создание номера")
async def create_room(hotel_id: int, room_data: RoomAdd = Body(openapi_examples={
    "1":{"summary":"Вип номер дубай", "value": {
        "title":"Вип-номер",
        "description":"Вип-номер в дубай резорт",
        "price":12600,
        "quantity":2

    }},
    "2":{"summary":"Простой номер сочи", "value": {
        "title":"Обычный-номер",
        "description":"Простой номер в сочи вилла",
        "price":2000,
        "quantity":12
    }}
    })
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data, hotel_id=hotel_id)
        await session.commit()

    return {"status":"ok", "data":room}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление номера")
async def put_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAdd,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status":"ok"}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status":"ok"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера")
async def patch_hotel(
    room_id: int,
    room_data: RoomPATCH
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True,id=room_id)
        await session.commit()
    return {"status":"ok"}