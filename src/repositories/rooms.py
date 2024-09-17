    
from sqlalchemy import func, insert, select
from schemas.rooms import Room, RoomAdd
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    async def add(self, data: RoomAdd, hotel_id):
        add_data_stmt = insert(RoomsOrm).values(**data.model_dump(), hotel_id=hotel_id).returning(RoomsOrm)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return Room.model_validate(model, from_attributes=True)
    
    async def get_all(self, hotel_id, title):
        query = select(RoomsOrm).filter(RoomsOrm.hotel_id==hotel_id)
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]