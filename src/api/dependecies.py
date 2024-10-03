from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request
import jwt
from pydantic import BaseModel

from services.auth import AuthService
from utils.db_manager import DBManager
from src.database import async_session_maker

class PaginationParams(BaseModel):
    page: Annotated[int  | None, Query(1, ge=1,description="Страница")]
    per_page: Annotated[int  | None, Query(None, ge=1, lt=100, description="Кол-во отелей на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int | None:
    data = AuthService().decode_token(token)
    return data.get("user_id", None)
    

UserIdDep = Annotated[int, Depends(get_current_user_id)]

def get_db_manager():
    return DBManager(session_factory=async_session_maker)

async def get_db():
    async with get_db_manager() as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]