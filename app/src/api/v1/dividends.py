import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.require_auth import verify_token
from src.celery_tasks.tasks import trade_extrinsic_ctask
from src.core.config import settings
from src.models.db import get_session
from src.models.dividends_history import DividendsHistory
from src.schemas.dividends import DividendsResponse
from src.services.dividends import get_tao_dividends

router = APIRouter()


@router.get('/tao_dividends', dependencies=[Depends(verify_token)])
async def tao_dividends(
        netuid: int = settings.DEFAULT_NETUID,
        hotkey: str = settings.DEFAULT_HOTKEY,
        trade: bool = False,
        session: AsyncSession = Depends(get_session),
) -> DividendsResponse:
    """
    Protected endpoint that returns the Tao dividends data for a given subnet and hotkey.
    Query parameters:
        - netuid (integer subnet ID)
        - hotkey (string account ID or public key)
        - trade (bool = False)

    Requires an Authorization header with the bearer token (or whatever auth scheme you choose).
    On success, returns a JSON response with the dividend value (and possibly a timestamp or other metadata).
    This call will also trigger a background stake operation on the blockchain,
    if trade=true query param was passed.
    """
    # Get dividends amount
    dividends = await get_tao_dividends(netuid, hotkey)
    now = datetime.datetime.utcnow()

    # Save historical data
    div_history = DividendsHistory(
        netuid=netuid,
        hotkey=hotkey,
        amount=dividends,
    )
    session.add(div_history)
    await session.commit()

    # Launch trading celery task in bg
    if trade:
        trade_extrinsic_ctask.delay(netuid, hotkey)

    return DividendsResponse(
        value=dividends,
        timestamp=now.isoformat(),
    )
