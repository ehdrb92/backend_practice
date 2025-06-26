from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DB: str
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int

    TEST_POSTGRESQL_USER: str
    TEST_POSTGRESQL_PASSWORD: str
    TEST_POSTGRESQL_DB: str
    TEST_POSTGRESQL_HOST: str
    TEST_POSTGRESQL_PORT: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()  # type: ignore
