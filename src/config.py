from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRESQL_USER: str = "dev"
    POSTGRESQL_PASSWORD: str = "dev"
    POSTGRESQL_DB: str = "dev"
    POSTGRESQL_HOST: str = "localhost"
    POSTGRESQL_PORT: int = 5432

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "algorithm"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
