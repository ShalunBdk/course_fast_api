from celery import Celery
from celery.schedules import crontab

from src.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks",
    ]
)

celery_instance.conf.beat_schedule = {
    "start every 5 minute": {
        "task": "booking_today_checkin",
        "schedule": crontab(hour=8),
    }
}