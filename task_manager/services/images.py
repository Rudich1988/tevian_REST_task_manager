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
    def __init__(
            self,
            image_repo: ImageRepository,
            statistic_service: StatisticService,
            file_operator: FileOperator,
            session: db_session
    ):
        self.image_repo= image_repo
        self.statistic_service = statistic_service
        self.file_operator = file_operator
        self.session = session

    def add_image(
            self,
            image_data: dict,
            file,
            faces_cloud_service: AbstractFaceCloudService
    ) -> dict:
        image = self.image_repo.add_one(image_data)
        self.file_operator.save(
            filepath=image_data['filepath'],
            image=file
        )
        faces_data = faces_cloud_service.detected_faces(
            file=image.filepath,
            image_id=image.id
        )
        if faces_data:
            FaceRepository(self.session).add_objects(data=faces_data)
            self.statistic_service.increment(
                task_id = image.task_id,
                data=faces_data,
                task_repo=TaskRepository(self.session)
            )
        return ImageSchema().dump(image)

    def get_image(self, image_data: dict) -> dict:
        image = self.image_repo.get_one(image_data)
        return ImageSchema().dump(image)

    def delete_image(self, image_data: dict) -> dict:
        image = self.image_repo.get_one(data=image_data)
        faces = ImageSchema().dump(image)['faces']
        filepath = ImageSchema().dump(image)['filepath']
        if faces:
            new_task_data = self.statistic_service.decrement(
                data=faces,
                task_repo=TaskRepository(self.session),
                task_id=image.task_id
            )
        count = self.image_repo.delete_one(image_data)
        self.file_operator.delete(files=[filepath])
        return {'success': f'Number of images deleted: {count}'}
