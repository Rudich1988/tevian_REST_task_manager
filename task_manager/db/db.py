from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from task_manager.config.base import Config


class ModelBase(DeclarativeBase):
    pass


engine = create_engine(Config.DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
