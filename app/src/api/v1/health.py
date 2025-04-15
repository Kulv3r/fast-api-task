from fastapi import APIRouter

from src.schemas.ping import PingResponse

router = APIRouter()


@router.get('/ping')
async def ping() -> PingResponse:
    return PingResponse(ping='pong')
