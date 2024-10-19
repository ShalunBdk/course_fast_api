from fastapi import APIRouter, Body

from fastapi_cache.decorator import cache


from src.schemas.facilities import FacilityAdd
from src.api.dependecies import DBDep
from src.tasks.tasks import test_task


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение удобств")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    return await db.facilities.get_all()


@router.post("", summary="Создание удобства")
async def create_facilities(
    db: DBDep,
    facility_data: FacilityAdd = Body(),
):
    facilitiy = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "ok", "data": facilitiy}
