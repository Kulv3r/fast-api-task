from celery import Celery

from src.core.config import settings


redis_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)
celery_app.autodiscover_tasks(['src.celery_tasks'], related_name='trade', force=True)
