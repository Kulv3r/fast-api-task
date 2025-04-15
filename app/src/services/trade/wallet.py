import logging

from bittensor_wallet import Wallet

logger = logging.getLogger(__name__)


def get_wallet() -> Wallet:
    """ Get a default wallet. """
    logger.info(f'Loading default wallet..')
    wallet = Wallet().create()
    logger.info(f'Wallet {wallet} has been loaded.')
    return wallet
