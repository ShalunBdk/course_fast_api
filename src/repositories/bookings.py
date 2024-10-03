from schemas.bookings import Booking
from src.repositories.base import BaseRepository
from models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking