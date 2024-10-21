from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound
from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: int,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        res = result.scalars().all()
        if not res:
            raise ObjectNotFoundException()
        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in res]

    async def get_one_with_rels(self, **filer_by):
        query = (
            select(self.model)
            .filter_by(**filer_by)
            .options(selectinload(self.model.facilities))
        )
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
