from datetime import date
from pydantic import BaseModel


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BaseModel):
    date_from: date
    date_to: date
    room_id: int
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int


class BookingPATCH(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    room_id: int | None = None
    user_id: int | None = None
    price: int | None = None
