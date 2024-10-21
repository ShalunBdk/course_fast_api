from fastapi import APIRouter, Response

from src.exceptions import (
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    NullPasswordException,
    NullPasswordHTTPException,
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
)
from src.api.dependecies import DBDep, UserIdDep
from src.services.auth import AuthService
from src.schemas.users import UserRequestAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/login", summary="Аутентефикация пользователя")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
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
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    except NullPasswordException:
        raise NullPasswordHTTPException

    return {"status": "ok"}


@router.get("/me", summary="Получить пользователя")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    return await AuthService(db).get_one_or_none(user_id)
