from task_manager.utils.repository import AbstractRepository
from task_manager.schemas.images import ImageSchemaAdd
from task_manager.db.db import Session
from task_manager.repositories.tasks import TaskRepository
from task_manager.repositories.faces import FaceRepository
from task_manager.services.tevian import TevianFaceCloudService
from task_manager.repositories.images import ImageRepository
from task_manager.services.statistic import StatisticService


class ImageService:
    def __init__(self, session: Session, image_repo=ImageRepository):
        self.image_repo: AbstractRepository = image_repo
        self.session: Session = session

    def add_image(
            self,
            image_data: dict,
            schema=ImageSchemaAdd,
            faces_cloud_service=TevianFaceCloudService,
            task_repo=TaskRepository,
            faces_repo=FaceRepository,
            statistic_service=StatisticService,
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
                if faces_data:
                    new_task_data = statistic_service().change_statistic(
                        task=task,
                        data=faces_data,
                        operator='+'
                    )
                task_repo(s).update_one(task, new_task_data)
            return schema().dump(image)

    def get_image(self, image_data: dict, schema=ImageSchemaAdd) -> dict:
        with self.session as s:
            image = self.image_repo(s).get_one(image_data)
            return schema().dump(image)

    def delete_image(
            self,
            image_data: dict,
            task_repo=TaskRepository,
            statistic_service=StatisticService,
            schema=ImageSchemaAdd
    ) -> dict:
        with self.session as s:
            image = self.image_repo(s).get_one(data=image_data)
            task = task_repo(s).get_one(data={'id': image.task_id})
            faces = schema().dump(image)['faces']
            if faces:
                new_task_data = statistic_service().change_statistic(
                    task=task,
                    data=faces,
                    operator='-'
                )
            task_repo(s).update_one(task, new_task_data)
            count = self.image_repo(s).delete_one(image_data)
            return {'success': f'Number of images deleted: {count}'}
