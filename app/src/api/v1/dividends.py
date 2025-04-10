from fastapi import APIRouter

from src.auth.require_auth import require_auth
from src.core.config import settings
from src.services.blockchain import get_tao_dividends

router = APIRouter()


@router.get('/tao_dividends')
@require_auth
async def tao_dividends(
        netuid: int = settings.DEFAULT_NETUID,
        hotkey: str = settings.DEFAULT_HOTKEY,
        trade: bool = False,
):
    dividends = await get_tao_dividends(netuid, hotkey)

    # if trade:
    #     stake_if_sentiment()
    return dividends
