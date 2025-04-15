from bittensor import AsyncSubtensor

from src.core.config import settings
from src.services.trade.wallet import get_wallet


def stake(netuid: int, hotkey: str, sentiment: int) -> None:
    """
    Stake Extrinsic & Sentiment-Based Adjustment
    For positive sentiment: add_stake (of amount .01 tao * sentiment score)
    For negative sentiment: unstake (of amount .01 tao * sentiment score)

    Args:
        netuid:
        hotkey:
        sentiment: sentiment score of recent tweets, from -100 to +100
    """
    if sentiment == 0:
        return

    wallet = get_wallet()
    amount = calc_amount(sentiment)

    with AsyncSubtensor(network=settings.DEFAULT_NET) as subtensor:
        if sentiment > 0:
            stake_method = subtensor.add_stake
        else:
            stake_method = subtensor.unstake

        stake_method(
            wallet=wallet,
            hotkey_ss58=hotkey,
            netuid=netuid,
            amount=amount,
        )


def calc_amount(sentiment: int) -> float:
    return abs(sentiment * 0.01)
