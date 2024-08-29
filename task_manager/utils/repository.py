from abc import ABC, abstractmethod

from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound

from task_manager.db.db import Session


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, session: Session):
        raise NotImplementedError

    @abstractmethod
    def add_one(self):
        raise NotImplementedError

    @abstractmethod
    def get_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, data: dict):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: Session):
        self.session = session

    def add_one(self, data: dict) -> int:
        obj = self.model(**data)
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_one(self, data: dict):
        obj = self.session.query(self.model).filter_by(**data)[0]
        return obj


    def delete_one(self, data: dict) -> int:
        stmt = delete(self.model)
        for key, value in data.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        result = self.session.execute(stmt)
        self.session.commit()
        count = result.rowcount
        if not count:
            raise NoResultFound
        return count
