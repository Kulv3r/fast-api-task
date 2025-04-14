from fastapi import APIRouter, Depends

from src.auth.require_auth import verify_token
from src.core.config import settings
from src.services.blockchain import get_tao_dividends

router = APIRouter()


@router.get('/tao_dividends', dependencies=[Depends(verify_token)])
async def tao_dividends(
        netuid: int = settings.DEFAULT_NETUID,
        hotkey: str = settings.DEFAULT_HOTKEY,
        trade: bool = False
):
    dividends = await get_tao_dividends(netuid, hotkey)

    # if trade:
    #     stake_if_sentiment()

    return dividends
