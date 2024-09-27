from task_manager.repositories.faces import FaceRepository
from task_manager.schemas.faces import FaceSchema


class FaceService:
    def __init__(
            self,
            face_repo: FaceRepository,
            schema: FaceSchema):
        self.face_repo = face_repo
        self.schema = schema

    def get_face(self, face_data: dict) -> dict:
        face = self.face_repo.get_one(face_data)
        return self.schema.dump(face)
