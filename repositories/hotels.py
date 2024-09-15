    
from sqlalchemy import func, insert, literal_column, select
from repositories.base import BaseRepository
from schemas.hotels import Hotel
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
        ):
            query = select(HotelsOrm)
            if location:
                query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
            if title:
                query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
            query = (
                query
                .limit(limit)
                .offset(offset)
            )
            result = await self.session.execute(query)
            return result.scalars().all()
    async def add(
            self,
            location,
            title,
        ):
            query = insert(HotelsOrm).values(location=location,title=title).returning(literal_column('*'))
            add_hotel_stmt = await self.session.execute(query)
            return  add_hotel_stmt.mappings().all()