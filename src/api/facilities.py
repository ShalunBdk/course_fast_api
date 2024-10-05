from fastapi import APIRouter, Body

from src.schemas.facilities import FacilityAdd
from src.api.dependecies import DBDep


router = APIRouter(prefix="/facilities",tags=["Удобства"])


@router.get("/", summary="Получение удобств")
async def get_facilities(
    db: DBDep,
):
    return await db.facilities.get_all()


@router.post("/", summary="Создание удобства")
async def create_facilities(
    db: DBDep,
    facility_data: FacilityAdd = Body(),
):
    facilitiy = await db.facilities.add(facility_data)
    await db.commit()
    return {"status":"ok", "data":facilitiy}