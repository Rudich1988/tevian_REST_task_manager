from task_manager.dto.faces import FaceResponseDTO
from task_manager.repositories.faces import FaceRepository


class FaceService:
    def __init__(
            self,
            face_repo: FaceRepository
    ):
        self.face_repo = face_repo

    def get_face(self, face_id: int) -> FaceResponseDTO:
        return self.face_repo.get_one(face_id=face_id)
