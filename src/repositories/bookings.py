from datetime import date
from sqlalchemy import select

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]
    
    async def add_booking(self, booking_data: BookingAdd):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=booking_data.date_from, date_to=booking_data.date_to)
        res = await self.session.execute(rooms_ids_to_get)
        if (booking_data.room_id in res.scalars().all()):
            booking = await self.add(booking_data)
            print(booking)
            return booking