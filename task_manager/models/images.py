from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task_manager.db.db import ModelBase


class Image(ModelBase):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    filename: Mapped[str] = mapped_column(String(500))
    unique_filename: Mapped[str] = mapped_column(String(500))
    filepath: Mapped[str] = mapped_column(String(500))
    task_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tasks.id",
            ondelete='CASCADE')
    )

    task: Mapped['Task'] = relationship(
        foreign_keys=[task_id],
        backref='images'
    )
