from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DB: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
