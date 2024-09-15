from fastapi import APIRouter

from passlib.context import CryptContext
import sqlalchemy

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        except sqlalchemy.exc.IntegrityError:
            return {"status":"email already exists"}
        await session.commit()
    
    return {"status":"ok"}