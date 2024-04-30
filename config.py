from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    BOT_TOKEN: str
    AMPLITUDE_API_KEY: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 5433
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
