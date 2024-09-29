from task_manager.schemas.images import ImageSchema, ImageResponseSchema
from task_manager.repositories.tasks import TaskRepository
from task_manager.repositories.faces import FaceRepository
from task_manager.schemas.tasks import TaskResponseSchema, TaskSchema
from task_manager.repositories.images import ImageRepository
from task_manager.services.statistic import StatisticService
from task_manager.services.file_operator import FileOperator
from task_manager.utils.services import AbstractFaceCloudService
from task_manager.db.db import db_session


class ImageService:
    def __init__(self, image_repo: ImageRepository):
        self.image_repo= image_repo

    def add_image(self, image_data: dict) -> dict:
        image = self.image_repo.add_one(image_data)
        return ImageSchema().dump(image)

    def get_image(self, image_data: dict) -> dict:
        image = self.image_repo.get_one(image_data)
        return ImageSchema().dump(image)

    def delete_image(self, image_data: dict) -> dict:
        self.image_repo.delete_one(image_data)
        return {"success": f"deleted image id: {image_data['id']}"}
