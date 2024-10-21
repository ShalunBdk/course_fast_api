from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.hotels import Hotel
from src.services.rooms import RoomsService
from src.services.base import BaseService


class BookingsService(BaseService):
    async def get_all(self):
        return await self.db.bookings.get_all()

    async def get_filtered(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, user_id: int, booking_data: BookingAddRequest):
        _room_data = await RoomsService(self.db).get_room_with_check(
            booking_data.room_id
        )
        hotel: Hotel = await self.db.hotels.get_one(id=_room_data.hotel_id)
        room_price = _room_data.price
        _booking_data = BookingAdd(
            user_id=user_id, price=room_price, **booking_data.model_dump()
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking
