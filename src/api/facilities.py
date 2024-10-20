from fastapi import APIRouter, Body

from fastapi_cache.decorator import cache


from src.services.facilities import FacilitiesService
from src.schemas.facilities import FacilityAdd
from src.api.dependecies import DBDep


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение удобств")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    return await FacilitiesService(db).get_all()


@router.post("", summary="Создание удобства")
async def create_facilities(
    db: DBDep,
    facility_data: FacilityAdd = Body(),
):
    facilitiy = await FacilitiesService(db).create_facilities(facility_data)

    return {"status": "ok", "data": facilitiy}
