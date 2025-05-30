import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api import routes
from src.api.deps import get_redis_client
from src.core.config import settings

logger = logging.getLogger(__name__)


app = FastAPI(
    title='fastapi-backend',
    description='base project for fastapi backend',
    version=settings.VERSION,
    openapi_url=f'/{settings.VERSION}/openapi.json',
)


def on_startup() -> None:
    redis_client = get_redis_client()
    FastAPICache.init(RedisBackend(redis_client), prefix='fastapi-cache')
    logger.info('FastAPI app running...')


app.add_middleware(CORSMiddleware, allow_origins=['*'])

app.add_event_handler('startup', on_startup)

app.include_router(routes.home_router)
app.include_router(routes.api_router, prefix=f'/api/{settings.VERSION}')
