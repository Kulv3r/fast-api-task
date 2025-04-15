from celery import Celery

from src.core.config import settings


redis_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)

# Include the tasks module
celery_app.conf.imports = (
    'src.celery_tasks.tasks',
)
