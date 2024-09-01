from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, Integer, Float

from task_manager.db.db import ModelBase


class Task(ModelBase):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(100))
    faces_counter: Mapped[int] = mapped_column(Integer, default=0)
    women_counter: Mapped[int] = mapped_column(Integer, default=0)
    male_counter: Mapped[int] = mapped_column(Integer, default=0)
    men_avg_age: Mapped[float] = mapped_column(Float, default=0.0)
    women_avg_age: Mapped[float] = mapped_column(Float, default=0.0)
