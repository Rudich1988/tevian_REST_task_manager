from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from task_manager.config.base import Config


class ModelBase(DeclarativeBase):
    pass


engine = create_engine(Config.DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)


def db_session():
    with Session() as session:
        yield session
