from typing import Any, Sequence
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ObjectNotFoundException
from src.database import Base
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filer_by) -> list[BaseModel | Any]:
        query = select(self.model).filter(*filter).filter_by(**filer_by)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs) -> list[BaseModel | Any]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filer_by) -> list[BaseModel | Any]:
        query = select(self.model).filter_by(**filer_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)
    
    async def get_one(self, **filer_by) -> BaseModel:
        query = select(self.model).filter_by(**filer_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> list[BaseModel | Any]:
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        try:
            result = await self.session.execute(add_data_stmt)
        except IntegrityError:
            raise ObjectNotFoundException
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: Sequence[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(data.model_dump(exclude_unset=exclude_unset))
        )
        result = await self.session.execute(update_stmt)
        if result.rowcount == 0:
            raise ObjectNotFoundException
        

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(delete_stmt)
        if result.rowcount == 0:
            raise ObjectNotFoundException
        
        
