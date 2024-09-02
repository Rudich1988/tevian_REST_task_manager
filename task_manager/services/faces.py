from task_manager.utils.repository import AbstractRepository
from task_manager.repositories.faces import FaceRepository
from task_manager.schemas.faces import FaceSchema
from task_manager.db.db import db_session


class FaceService:
    def __init__(
            self,
            session=db_session,
            face_repo=FaceRepository,schema=FaceSchema):
        self.face_repo: AbstractRepository = face_repo
        self.session = session
        self.schema = schema

    def get_face(self, face_data: dict) -> dict:
        with self.session() as s:
            face = self.face_repo(s).get_one(face_data)
            return self.schema().dump(face)
