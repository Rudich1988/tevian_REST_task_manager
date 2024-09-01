from marshmallow import EXCLUDE

from task_manager.utils.repository import AbstractRepository
from task_manager.schemas.images import ImageSchemaAdd
from task_manager.db.db import Session
from task_manager.services.faces import FaceService
from task_manager.utils.services import AbstractFaceCloudService
from task_manager.repositories.tasks import TaskRepository
from task_manager.services.tasks import TaskService
from task_manager.repositories.faces import FaceRepository
from task_manager.schemas.tasks import TaskSchemaAdd


class ImageService:
    def __init__(self, image_repo: AbstractRepository, session: Session):
        self.image_repo: AbstractRepository = image_repo
        self.session: Session = session

    def add_image(
            self,
            image_data: dict,
            schema: ImageSchemaAdd,
            faces_cloud_service: AbstractFaceCloudService,
            task_repo=TaskRepository,
            faces_repo=FaceRepository,
            task_service=TaskService,
    ) -> dict:
        with self.session as s:
            image = self.image_repo(s).add_one(image_data)
            faces_data = faces_cloud_service().detected_faces(
                filename=image.filename,
                image_id=image.id
            )
            if faces_data:
                faces_repo(session=s).add_objects(data=faces_data)
                task = task_repo(s).get_one({'id': image.task_id})
                new_task_data = task_service(s).change_statistic(
                    task=task,
                    data=faces_data,
                    operator='+'
                )
                task_repo(s).update_one(task, new_task_data)
            return schema().dump(image)

    def get_image(self, image_data: dict, schema: ImageSchemaAdd) -> dict:
        with self.session as s:
            image = self.image_repo(s).get_one(image_data)
            return schema().dump(image)

    def delete_image(self, image_data: dict) -> dict:
        with self.session as s:
            count = self.image_repo(s).delete_one(image_data)
            return {'success': f'Number of images deleted: {count}'}
