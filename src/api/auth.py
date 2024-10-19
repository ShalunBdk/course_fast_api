from fastapi import APIRouter, HTTPException, Response

import sqlalchemy

from src.api.dependecies import DBDep, UserIdDep
from src.services.auth import AuthService
from src.schemas.users import UserAdd, UserRequestAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/login", summary="Аутентефикация пользователя")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep,
):
    try:
        user = await db.users.get_user_with_hashed_password(email=data.email)
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль не верный")
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=401, detail="Пользователь с таким email не зарегистрирован"
        )
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout", summary="Выход пользователя")
async def logout(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "ok"}


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    if not data.password:
        raise HTTPException(status_code=400, detail="Введён пустой пароль")
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(new_user_data)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Пользвоталь с таким email уже зарегистрирован"
        )
    await db.commit()

    return {"status": "ok"}


@router.get("/me", summary="Получить пользователя")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    user = await db.users.get_one_or_none(id=user_id)
    return user
