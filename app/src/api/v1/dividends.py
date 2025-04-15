from fastapi import APIRouter, Depends

from src.auth.require_auth import verify_token
from src.celery_tasks.trade import trade_extrinsic_ctask
from src.core.config import settings
from src.services.dividends import get_tao_dividends

router = APIRouter()


@router.get('/tao_dividends', dependencies=[Depends(verify_token)])
async def tao_dividends(
        netuid: int = settings.DEFAULT_NETUID,
        hotkey: str = settings.DEFAULT_HOTKEY,
        trade: bool = False,
):
    dividends = await get_tao_dividends(netuid, hotkey)

    if trade:
        trade_extrinsic_ctask.delay(netuid, hotkey)

    return dividends
