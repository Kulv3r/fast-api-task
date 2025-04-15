from src.services.datura_tweets import search_twitter
from src.services.sentiment import get_sentiment

from src.services.trade.stake import stake


def trade_extrinsic(netuid: int, hotkey: str) -> None:
    """
    Does stake/unstake operations based on Twitter sentiment:
        - Queries Twitter via Datura.ai API for tweets about the subnet
        - Analyzes tweet sentiment using Chutes.ai LLM
        - Stakes or unstakes TAO proportional to sentiment score (-100 to +100)

    Args:
        netuid:
        hotkey:
    """
    recent_tweets = search_twitter(netuid)
    sentiment = get_sentiment(recent_tweets)
    stake(netuid, hotkey, sentiment)
