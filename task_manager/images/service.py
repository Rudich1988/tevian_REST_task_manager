from task_manager.images.repository import ImageRepository
from task_manager.images.dto import ImageDTO, ImageDataDTO
from task_manager.db.db import Session
from task_manager.tasks.repository import TaskRepository
from task_manager.statistic.task_statistic import StatisticService
from task_manager.images_analyzers.tevian import TevianFaceCloudService
from task_manager.faces.repository import FaceRepository


class ImageService:
    def __init__(self, image_repo: ImageRepository):
        self.image_repo= image_repo

    def add_image(
            self,
            image_data: ImageDataDTO,
            file,
            session: Session
    ) -> ImageDTO:
        image_data = self.image_repo.add_one(image_data)
        faces_data = TevianFaceCloudService().detected_faces(
            file=file,
            image_id=image_data.id)
        if faces_data:
            faces = (FaceRepository(session).add_faces(
                faces_data=faces_data)
            )
            StatisticService().increment(
                task_id=image_data.task_id,
                faces_data=faces_data,
                task_repo=TaskRepository(session)
            )
            image_data.faces.extend(faces)
        return image_data


    def get_image(self, image_id: int) -> ImageDTO:
        return self.image_repo.get_one(image_id=image_id)

    def delete_image(self, image_id: int) -> None:
        self.image_repo.delete_one(image_id)
