from bittensor_wallet import Wallet

from src.core.config import settings


def init_wallet() -> Wallet:
    """
    Creates a wallet and stores keys at:
        /Users/you/.bittensor/wallets/default/coldkey
        /Users/you/.bittensor/wallets/default/coldkeypub.txt
    """
    wallet = Wallet()
    wallet.regenerate_coldkey(
        mnemonic=settings.DEFAULT_MNEMONIC,
        coldkey_password=settings.WALLET_COLDKEY_PASSWORD,
    )
    return wallet


def get_wallet() -> Wallet:
    """ Get default existing wallet. """
    return Wallet().create()
