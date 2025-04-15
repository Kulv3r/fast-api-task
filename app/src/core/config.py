import logging
from typing import Any, Optional, Union

from pydantic import AnyHttpUrl, Field, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    LOG_LEVEL: int = Field(default=logging.INFO)

    VERSION: str = Field(default='v1')
    DEBUG: bool = Field(default=True)

    DEFAULT_HOTKEY: str = Field()
    DEFAULT_NETUID: int = Field()
    DEFAULT_NET: str = Field(default='test')
    AUTH_TOKEN: str = Field()

    POSTGRES_USER: str = Field(default='')
    POSTGRES_PASSWORD: str = Field(default='')
    POSTGRES_HOST: str = Field(default='')
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field(default='')
    POSTGRES_URL: Union[Optional[PostgresDsn], Optional[str]] = None

    @field_validator('POSTGRES_URL', mode='before')
    @classmethod
    def build_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str) and len(v) > 0:
            return v

        url = PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=values.data.get('POSTGRES_USER'),
            password=values.data.get('POSTGRES_PASSWORD'),
            host=values.data.get('POSTGRES_HOST'),
            port=values.data.get('POSTGRES_PORT'),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        ).unicode_string()
        return url

    REDIS_HOST: str = Field(default='')
    REDIS_PORT: str = Field(default='')

    DATURA_API_KEY: str = Field()
    CHUTES_API_KEY: str = Field()


settings = Settings()
