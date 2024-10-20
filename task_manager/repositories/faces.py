from dataclasses import asdict
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from task_manager.models.faces import Face
from task_manager.utils.repository import SQLAlchemyRepository
from task_manager.dto.faces import FaceDataDTO, FaceResponseDTO, FaceDTO


class FaceRepository(SQLAlchemyRepository):
    model = Face

    def create_face_dto(self, face) -> FaceDTO:
        return FaceDTO(
            age=face.age,
            gender=face.gender,
            bounding_box=face.bounding_box
        )

    def create_face_response_dto(
            self,
            face
    ) -> FaceResponseDTO:
        return FaceResponseDTO(
            id=face.id,
            image_id=face.image_id,
            age=face.age,
            gender=face.gender,
            bounding_box=face.bounding_box
        )

    def get_one(self, face_id: int) -> FaceResponseDTO:
        stmt = select(self.model).where(
            self.model.id == face_id
        )
        result = self.session.execute(stmt)
        face = result.scalars().first()
        if not face:
            raise NoResultFound
        return self.create_face_response_dto(face)

    def add_faces(
            self,
            faces_data: list[Optional[FaceDataDTO]]
    ) -> list[FaceDTO]:
        faces = [
            self.model(
                **asdict(face_data, dict_factory=dict)
            ) for face_data in faces_data
        ]
        self.session.add_all(faces)
        self.session.flush()
        faces_data = []
        for face in faces:
            face = self.create_face_dto(face)
            faces_data.append(face)
        return faces_data
