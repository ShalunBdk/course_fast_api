

from sqlalchemy import insert, select


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filer_by):
        query = select(self.model).filter_by(**filer_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, *args, **kwargs):
        query = insert(self.model)
        add_hotel_stmt = insert(self.model).values(*args)
        result = await self.session.execute(add_hotel_stmt)
        return result