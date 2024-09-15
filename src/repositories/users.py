    
from schemas.users import User
from src.repositories.base import BaseRepository
from src.models.users import UsersOrm


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User