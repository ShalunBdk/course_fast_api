from schemas.bookings import Booking
from src.schemas.facilities import Facilities
from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities