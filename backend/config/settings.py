from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(default="development", alias="APP_ENV")
    app_name: str = Field(default="crypto-bot", alias="APP_NAME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    default_symbol: str = Field(default="BTCUSDT", alias="DEFAULT_SYMBOL")
    default_timeframe: str = Field(default="5m", alias="DEFAULT_TIMEFRAME")

    bybit_api_key: str = Field(default="", alias="BYBIT_API_KEY")
    bybit_api_secret: str = Field(default="", alias="BYBIT_API_SECRET")
    bybit_testnet: bool = Field(default=True, alias="BYBIT_TESTNET")
    bybit_base_url: str = Field(default="https://api-testnet.bybit.com", alias="BYBIT_BASE_URL")

    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/crypto_bot",
        alias="DATABASE_URL",
    )


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()