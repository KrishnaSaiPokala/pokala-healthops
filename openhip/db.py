from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from openhip.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.db_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    from openhip import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def reset_db() -> None:
    from openhip import models  # noqa: F401

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
