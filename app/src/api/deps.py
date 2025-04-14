from redis import asyncio as aioredis

from src.core.config import settings


def get_redis_client() -> aioredis:
    redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
        max_connections=10,
    )
    return redis
