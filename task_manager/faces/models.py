from sqlalchemy import BigInteger, ForeignKey, String, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task_manager.db.db import ModelBase


class Face(ModelBase):
    __tablename__ = 'faces'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    bounding_box: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )
    gender: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey(
            "images.id",
            ondelete='CASCADE'
        ),
        index=True
    )
    age: Mapped[float] = mapped_column(Float, nullable=False)

    image: Mapped['Image'] = relationship(
        foreign_keys=[image_id],
        back_populates='faces'
    )
