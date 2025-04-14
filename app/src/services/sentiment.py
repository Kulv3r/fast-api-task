import json
import logging
from typing import List

import requests

from src.core.config import settings

logger = logging.getLogger(__name__)

# Prompt for LLM
# Note that "analysis" field is not actually used later on,
# but forcing LLM to defend it's point usually improves the numeric value accuracy it gives.
PROMPT_TEMPLATE = '''
Analyze the sentiment of the following tweets 
and provide a single aggregated sentiment score on a scale from -100 to +100, where:
- -100 means extremely negative
- 0 means neutral
- +100 means extremely positive

Consider the overall tone, language, and emotional content of all tweets together. 
Provide your score along with a brief 1-2 sentence explanation of your reasoning.

Tweets:
"""
%s
"""

Your response should be a **valid JSON** like:
```
{
    score: [int sentiment score here],
    analysis: [brief explanation]
}
```
'''
URL = 'https://llm.chutes.ai/v1/chat/completions'
MODEL = 'unsloth/Llama-3.2-3B-Instruct'
TEMPERATURE = 0.5

# Upper limit as 280 (max chars in 1 tweet) by 10 tweets (amount we get from Datura API):
MAX_TWEETS_STR_LEN = 280 * 10

MAX_ATTEMPTS = 10


class ChutesAPIError(Exception):
    pass


def get_sentiment(tweets: List[str]) -> int:
    """
    Feeds tweets into Chutes.ai API for a llama LLM v3
    to get a sentiment score (-100 to +100) from the tweets.

    Args:
        tweets: A list of string tweet texts to get overall sentiment for.

    Returns:
        An int from -100 to +100.
    """
    if not tweets:
        return 0

    tweets_joined = '\n'.join(tweets)[:MAX_TWEETS_STR_LEN]

    headers = {
        'Authorization': f'Bearer {settings.CHUTES_API_KEY}',
        'Content-Type': 'application/json',
    }
    params = {
        'model': 'unsloth/Llama-3.2-3B-Instruct',
        'messages': [
            {
                'role': 'system',
                'content': 'Always respond with **strictly valid JSON only**.',
            },
            {
                'role': 'user',
                'content': PROMPT_TEMPLATE % tweets_joined,
            }
        ],
        'stream': False,
        'temperature': TEMPERATURE,
    }
    for attempt in range(MAX_ATTEMPTS):
        try:
            response = requests.post(URL, json=params, headers=headers)
            response.raise_for_status()
            resp_json = response.json()['choices'][0]['message']['content'].replace("```", '').strip()
            resp_json_parsed = json.loads(resp_json)
            break
        except (requests.RequestException, json.JSONDecodeError, KeyError, IndexError) as e:
            logger.warning(f'Failed to get data from Chutes.ai API: {e}')
            if attempt + 1 == MAX_ATTEMPTS:
                raise ChutesAPIError(
                    f'Failed to get data from Chutes.ai API after {MAX_ATTEMPTS} attempts.'
                ) from e

    sentiment = resp_json_parsed['score']
    return sentiment
