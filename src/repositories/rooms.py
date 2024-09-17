    
from sqlalchemy import func, insert, select
from schemas.rooms import Room, RoomAdd
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room
