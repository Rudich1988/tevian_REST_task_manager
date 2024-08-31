from email.policy import default
from os.path import defpath

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, Integer

from task_manager.db.db import ModelBase


class Task(ModelBase):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    #title: Mapped[str] = mapped_column(String(100))
    #faces_counter: Mapped[int] = mapped_column(Integer, default=0)
    #women_counter: Mapped[[int]] = mapped_column(Integer, default=0)



