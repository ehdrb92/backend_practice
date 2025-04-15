from sqlmodel import create_engine, Session

from config import get_settings

settings = get_settings()

engine = create_engine(f"postgresql+psycopg2://{settings.POSTGRESQL_USER}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_DB}")


def get_session():
    with Session(engine) as session:
        yield session
