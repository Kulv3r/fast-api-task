import asyncio
import logging
from asyncio import sleep
from typing import Optional

# from bittensor import AsyncSubtensor
from fastapi_cache.decorator import cache

logger = logging.getLogger(__name__)


# @cache(expire=60 * 2)
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
    # todo: del
    logger.warning(f'FAKE API CALL HERE')
    await sleep(1)
    from random import randint
    return randint(0, 100)
    # logger.info(f'Quering the TaoDividendsPerSubnet for a given {hotkey=} and {netuid=}...')
    # async with AsyncSubtensor(network=settings.DEFAULT_NET) as subtensor:
    #     result = await subtensor.query_subtensor(
    #         name='TaoDividendsPerSubnet',
    #         params=[netuid, hotkey],
    #     )
    #     logger.info(f'Got {result=}, {result.value=}')
    #     return result.value


# Example usage:
async def main():
    hotkey_ss58 = '5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v'
    netuid = 18

    dividends = await get_tao_dividends(netuid, hotkey_ss58)
    print(f'Last dividends for hotkey {hotkey_ss58} on subnet {netuid}: {dividends}')


if __name__ == '__main__':
    asyncio.run(main())
