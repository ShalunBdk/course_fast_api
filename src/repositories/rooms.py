from datetime import date

from sqlalchemy import select, func
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomAdd
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room
    

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: int,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))

        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))