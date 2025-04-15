from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = AsyncEngine(
    create_engine(
        settings.POSTGRES_URL,
        echo=settings.DEBUG,
        future=True,
    )
)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
