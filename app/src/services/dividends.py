import logging

from bittensor import AsyncSubtensor
from fastapi_cache.decorator import cache

from src.core.config import settings

logger = logging.getLogger(__name__)


@cache(expire=2, namespace='tao-dividends')
async def get_tao_dividends(
        netuid: int,
        hotkey: str,
) -> int:
    """
    Queries the TaoDividendsPerSubnet for a given subnet and hotkey.

    Args:
        netuid: The subnet ID to query
        hotkey: The SS58 address of the hotkey to query

    Returns:
        The last total dividend for the hotkey on the subnet, or None if not found
    """
    logger.info(f'Quering the TaoDividendsPerSubnet for a given {hotkey=} and {netuid=}...')
    async with AsyncSubtensor(network=settings.DEFAULT_NET) as subtensor:
        result = await subtensor.query_subtensor(
            name='TaoDividendsPerSubnet',
            params=[netuid, hotkey],
        )
        logger.info(f'Got TaoDividendsPerSubnet {result=}, {result.value=}')
        return result.value
