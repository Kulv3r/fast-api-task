from pydantic import BaseModel, Field


class DividendsResponse(BaseModel):
    value: int
    timestamp: str = Field(..., description='ISO format.')
