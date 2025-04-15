from src.models.base import BaseModel


class DividendsHistory(BaseModel, table=True):
    netuid: int
    hotkey: str
    amount: int
