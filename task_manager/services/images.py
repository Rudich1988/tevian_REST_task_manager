from task_manager.schemas.images import ImageSchemaAdd
from task_manager.db.db import Session
from task_manager.db.db import db_session
from task_manager.repositories.tasks import TaskRepository
from task_manager.repositories.faces import FaceRepository
from task_manager.services.tevian import TevianFaceCloudService
from task_manager.repositories.images import ImageRepository
from task_manager.services.statistic import StatisticService
from task_manager.services.file_operator import FileOperator


class ImageService:
    def __init__(
            self,
            session=db_session,
            image_repo=ImageRepository,
            faces_cloud_service=TevianFaceCloudService,
            faces_repo=FaceRepository,
            statistic_service=StatisticService,
            task_repo=TaskRepository,
            schema=ImageSchemaAdd(),
            file_operator=FileOperator
    ):
        self.image_repo= image_repo
        self.session: Session = session
        self.faces_cloud_service = faces_cloud_service
        self.faces_repo = faces_repo
        self.statistic_service = statistic_service
        self.task_repo = task_repo
        self.schema = schema
        self.file_operator = file_operator()

    def add_image(self, image_data: dict) -> dict:
        with self.session() as s:
            image = self.image_repo(s).add_one(image_data)
            faces_data = self.faces_cloud_service().detected_faces(
                file=image.filepath,
                image_id=image.id
            )
            if faces_data:
                self.faces_repo(session=s).add_objects(data=faces_data)
                self.statistic_service().increment(
                    task_id = image.task_id,
                    data=faces_data,
                    task_repo=self.task_repo(s)
                )
            return self.schema.dump(image)

    def get_image(self, image_data: dict) -> dict:
        with self.session() as s:
            image = self.image_repo(s).get_one(image_data)
            return self.schema.dump(image)

    def delete_image(self, image_data: dict) -> dict:
        with self.session() as s:
            image = self.image_repo(s).get_one(data=image_data)
            faces = self.schema.dump(image)['faces']
            filepath = self.schema.dump(image)['filepath']
            if faces:
                new_task_data = self.statistic_service().decrement(
                    data=faces,
                    task_repo=self.task_repo(s),
                    task_id=image.task_id
                )
            count = self.image_repo(s).delete_one(image_data)
            self.file_operator.delete(filepath)
            return {'success': f'Number of images deleted: {count}'}
