
from fastapi import APIRouter, HTTPException, Response

import sqlalchemy

from services.auth import AuthService
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from schemas.users import UserAdd, UserRequestAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/login", summary="Аутентефикация пользователя")
async def login_user(
    data: UserRequestAdd,
    response: Response,
):
    # hashed_password = pwd_context.hash(data.password)
    # new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользвоталь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль не верный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=400, detail="Пользвоталь с таким email уже зарегистрирован")
        await session.commit()
    
    return {"status":"ok"}