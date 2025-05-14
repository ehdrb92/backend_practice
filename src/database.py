from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import get_settings

settings = get_settings()

engine = create_engine(
    f"postgresql+psycopg2://{settings.POSTGRESQL_USER}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_HOST}:{settings.POSTGRESQL_PORT}/{settings.POSTGRESQL_DB}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_session():
    return SessionLocal()
