from dataclasses import asdict
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import raiseload, joinedload
from sqlalchemy.exc import NoResultFound

from task_manager.images.models import Image
from task_manager.utils.repository import SQLAlchemyRepository
from task_manager.images.dto import ImageDTO, ImageDataDTO
from task_manager.faces.repository import FaceRepository


class ImageRepository(SQLAlchemyRepository):
    model = Image

    def create_image_dto(
            self,
            image
    ) -> ImageDTO:
        faces = []
        if image.faces:
            for face in image.faces:
                faces.append(
                    FaceRepository(
                        session=self.session
                    ).create_face_dto(face)
                )
        return ImageDTO(
            id=image.id,
            filename=image.filename,
            faces=faces,
            unique_filename=image.unique_filename,
            task_id=image.task_id,
            filepath=image.filepath
        )

    def get_one(self, image_id: int) -> ImageDTO:
        query = (
            select(self.model)
            .where(self.model.id == image_id)
            .options(joinedload(self.model.faces))
        )
        image = self.session.execute(query).scalars().first()
        if not image:
            raise NoResultFound
        return self.create_image_dto(image=image)

    def get_files(self, task_id: int) -> list[Optional[str]]:
        query = (
            select(self.model)
            .options(raiseload(self.model.faces))
            .where(self.model.task_id == task_id)
        )
        files = self.session.execute(query)
        return [row.filepath for row in files.scalars()]

    def add_one(self, image_data: ImageDataDTO) -> ImageDTO:
        image = self.model(
            **asdict(image_data, dict_factory=dict)
        )
        image.faces = []
        self.session.add(image)
        self.session.flush()
        return self.create_image_dto(image)

    def delete_one(self, image_id: int) -> None:
        stmt = delete(self.model).where(self.model.id == image_id)
        result = self.session.execute(stmt)
        if result.rowcount == 0:
            raise NoResultFound
