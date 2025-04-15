from src import celery_app
from src.services.trade.trade import trade_extrinsic


@celery_app.task
def trade_extrinsic_ctask(netuid: int, hotkey: str) -> None:
    trade_extrinsic(netuid, hotkey)
