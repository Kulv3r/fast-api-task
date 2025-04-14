import json
import logging
from typing import List

import requests
from src.core.config import settings


logger = logging.getLogger(__name__)

URL = 'https://apis.datura.ai/twitter'
MAX_ATTEMPTS = 10


class TwitterError(Exception):
    pass


def search_twitter(netuid: int) -> List[str]:
    """
    Search Twitter/X via Datura API for tweets related to a given netuid.

    Args:
        netuid: The subnet ID to query

    Returns:
        A [list] of tweets as str texts. The rest of tweet data is discarded.
    """
    headers = {
        'Authorization': settings.DATURA_API_KEY,
        'Content-Type': 'application/json'
    }
    params = {
        'query': f'Bittensor netuid {netuid}',
        'lang': 'en',
        'sort': 'Top',
        'count': 10,
    }
    for attempt in range(MAX_ATTEMPTS):
        try:
            response = requests.get(URL, params=params, headers=headers)
            response.raise_for_status()
            break
        except (requests.RequestException, json.JSONDecodeError) as e:
            logger.warning(f'Failed to get data from Twitter via Datura API: {e}')
    else:
        raise TwitterError(f'Failed to get data from Twitter after {MAX_ATTEMPTS} attempts.')

    tweets = [t['text'] for t in response.json()]
    return tweets
