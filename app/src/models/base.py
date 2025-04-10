from datetime import datetime
from typing import Optional

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlmodel import Column, DateTime, Field, SQLModel


# https://docs.sqlalchemy.org/en/20/core/compiler.html#utc-timestamp-function
class utcnow(expression.FunctionElement):  # type: ignore
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')  # type: ignore
def pg_utcnow(element, compiler, **kw) -> str:
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class BaseModel(SQLModel):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
    )
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=utcnow(),
            nullable=True,
        )
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=utcnow(),
            nullable=True,
        ),
    )
    deleted_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
