from task_manager.utils.repository import AbstractRepository
from task_manager.schemas.faces import FaceSchema
from task_manager.db.db import Session


class FaceService:
    def __init__(self,
                 face_repo: AbstractRepository,
                 session: Session
                 ):
        self.face_repo: AbstractRepository = face_repo
        self.session: Session = session

    def add_face(self,
                 face_data: dict,
                 schema: FaceSchema
                 ) -> dict:
        with self.session as s:
            face = self.face_repo(s).add_one(face_data)
            return schema().dump(face)

    def get_face(self,
                 face_data: dict,
                 schema: FaceSchema
                 ) -> dict:
        with self.session as s:
            face = self.face_repo(s).get_one(face_data)
            return schema().dump(face)

    def delete_face(self,
                    face_data: dict
                    ) -> dict:
        with self.session as s:
            count = self.face_repo(s).delete_one(face_data)
            return {'success': f'Number of face deleted: {count}'}
