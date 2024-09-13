from fastapi import Query, APIRouter, Body
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels",tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name":"sochi"},
    {"id": 2, "title": "Дубай", "name":"dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]



@router.get("/", summary="Получение отелей")
def get_hotels(
    id: int | None = Query(None, description="Айди отеля"),
    title: str | None = Query(None, description="Название отеля"),
    page: int  | None = Query(1, description="Страница"),
    per_page: int  | None = Query(3, description="Кол-во отелей на странице")
):
    hotels_ = []
    index = per_page * page
    for hotel in hotels[index-per_page:index]:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

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
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1":{"summary":"Сочи", "value": {
        "title":"Отель сочи 5 звезд у моря",
        "name":"sochi_u_morya"
    }},
    "2":{"summary":"Дубай", "value": {
        "title":"Отель дубай у фонтана",
        "name":"dubai_fontain"
    }}
    })
):
    global hotels
    hotels.append({
        "id":hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status":"ok"}
