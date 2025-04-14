from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response


router = APIRouter()


@router.get('/ping')
async def ping() -> Response:
    return JSONResponse({'ping': 'pong'})
