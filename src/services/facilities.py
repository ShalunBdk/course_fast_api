

from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilitiesService(BaseService):

    async def get_all(self):
        return await self.db.facilities.get_all()
    
    async def create_facilities(self, data: FacilityAdd):
        facilitiy = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()

        return facilitiy
