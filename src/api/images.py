from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService


router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("/", summary="Загрузка изображения")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image(file, background_tasks)
    return {"status": "ok"}
