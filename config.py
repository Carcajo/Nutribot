from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    BOT_TOKEN: str
    AMPLITUDE_API_KEY: str
    REDIS_HOST: ClassVar[str] = "localhost"
    REDIS_PORT: int = 6379
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
