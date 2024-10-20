from abc import ABC, abstractmethod

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

    def add_one(self, object_id: int):
        pass

    def get_one(self, object_id: int):
        pass

    def delete_one(self, object_id: int) -> None:
        pass
