from datetime import date

from sqlalchemy import delete, insert, select, func
from src.models.facilities import RoomsFacilitiesOrm
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
    
    async def edit_facilities(
            self,
            room_id,
            facilities_ids: list[int]
    ):

        delete_facilities_stmt = (
            delete(RoomsFacilitiesOrm)
            .where(RoomsFacilitiesOrm.room_id == room_id)
            .where(RoomsFacilitiesOrm.facility_id.notin_(facilities_ids))
        )
        await self.session.execute(delete_facilities_stmt)

        existing_facilities_stmt = (
            select(RoomsFacilitiesOrm.facility_id)
            .where(RoomsFacilitiesOrm.room_id == room_id)
        )
        existing_facilities_result = await self.session.execute(existing_facilities_stmt)
        existing_facilities = {row.facility_id for row in existing_facilities_result}

        new_facility_ids_set = set(facilities_ids)  # множество новых удобств
        existing_facilities_set = set(existing_facilities)  # множество существующих удобств

        facilities_to_add = new_facility_ids_set - existing_facilities_set

        if facilities_to_add:
            add_facilities_stmt = insert(RoomsFacilitiesOrm).values([{
                'room_id': room_id,
                'facility_id': facility_id
            } for facility_id in facilities_to_add])
            await self.session.execute(add_facilities_stmt)