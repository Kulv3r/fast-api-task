from fastapi import Request, HTTPException
from functools import wraps

from src.core.config import settings


def require_auth(route):
    @wraps(route)
    async def wrapper(request: Request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token != settings.AUTH_TOKEN:
            raise HTTPException(status_code=401, detail='Unauthorized.')
        return await route(request, *args, **kwargs)
    return wrapper
