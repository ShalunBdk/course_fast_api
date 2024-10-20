

from datetime import date
from fastapi import APIRouter, Body, Query

from src.services.rooms import RoomsService
from src.exceptions import HotelNotFoundException, HotelNotFoundHTTPException, ObjectNotFoundException, RoomNotFoundException, RoomNotFoundHTTPException
from src.api.dependecies import DBDep
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение номеров")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples="2024-10-05"),
    date_to: date = Query(examples="2024-10-06"),
):
    try:
        return await RoomsService(db).get_filtered_by_time(hotel_id, date_from, date_to)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по ID")
async def get_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        return RoomsService(db).get_one_with_rels(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Создание номера")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Вип номер дубай",
                "value": {
                    "title": "Вип-номер",
                    "description": "Вип-номер в дубай резорт",
                    "price": 12600,
                    "quantity": 2,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Простой номер сочи",
                "value": {
                    "title": "Обычный-номер",
                    "description": "Простой номер в сочи вилла",
                    "price": 2000,
                    "quantity": 12,
                    "facilities_ids": [],
                },
            },
        }
    ),
):    
    try:
        room = await RoomsService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление номера")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
    db: DBDep,
):
    try:
        await RoomsService(db).edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep,
):
    try:
        await RoomsService(db).partially_edit_room(hotel_id, room_id, room_data, exclude_unset=True)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        await RoomsService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "ok"}
