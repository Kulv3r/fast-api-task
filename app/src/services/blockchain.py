import asyncio
import logging

from bittensor import AsyncSubtensor
from typing import Optional

from fastapi_cache.decorator import cache

logger = logging.getLogger(__name__)


@cache(expire=60*2)
async def get_tao_dividends(
        netuid: int,
        hotkey: str,
        block: Optional[int] = None,
        block_hash: Optional[str] = None,
        reuse_block: bool = False
) -> Optional[int]:
    """
    Queries the TaoDividendsPerSubnet for a given subnet and hotkey.

    Args:
        netuid: The subnet ID to query
        hotkey: The SS58 address of the hotkey to query
        block: Optional block number to query at
        block_hash: Optional block hash to query at
        reuse_block: Whether to reuse the last-used block

    Returns:
        The last total dividend for the hotkey on the subnet, or None if not found
    """
    logger.info(f'Quering the TaoDividendsPerSubnet for a given {hotkey=} and {netuid=}...')
    async with AsyncSubtensor(network='test') as subtensor:
        # Determine the block hash to use
        block_hash = await subtensor.determine_block_hash(block, block_hash, reuse_block)
        logger.info(f'Got {block_hash=}')

        # Query the TaoDividendsPerSubnet storage
        result = await subtensor.query_subtensor(
            name='TaoDividendsPerSubnet',
            params=[netuid, hotkey],
            block=block,
            block_hash=block_hash,
            reuse_block=reuse_block
        )
        logger.info(f'Got {result=}, {result.value=}')
        return result.value


# Example usage:
async def main():
    hotkey_ss58 = '5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v'
    netuid = 18

    dividends = await get_tao_dividends(netuid, hotkey_ss58)
    print(f'Last dividends for hotkey {hotkey_ss58} on subnet {netuid}: {dividends}')


if __name__ == '__main__':
    asyncio.run(main())
