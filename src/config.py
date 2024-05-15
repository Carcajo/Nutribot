from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    BOT_TOKEN: str
    AMPLITUDE_API_KEY: str
    REDIS_HOST: ClassVar[str] = "redis"
    REDIS_PORT: int = 6379
    DATABASE_URL: str
    DATABASE_URL_ASYNC: str

    class Config:
        extra = 'ignore'
        env_file = ".env"
        env_file_encoding = "utf-8"

SETTINGS = Settings()
