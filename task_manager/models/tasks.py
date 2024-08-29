from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String

from task_manager.db.db import ModelBase


class Task(ModelBase):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(BigInteger,
                                    primary_key=True,
                                    autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
