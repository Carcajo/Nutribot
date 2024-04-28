from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TELEGRAM_BOT_TOKEN: str
    AMPLITUDE_API_KEY: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 5432
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()