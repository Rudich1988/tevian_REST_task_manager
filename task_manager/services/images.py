from task_manager.utils.repository import AbstractRepository
from task_manager.schemas.images import ImageSchemaAdd
from task_manager.db.db import Session
from task_manager.services.faces import FaceService
from task_manager.utils.services import AbstractFaceCloudService


class ImageService:
    def __init__(self, image_repo: AbstractRepository, session: Session):
        self.image_repo: AbstractRepository = image_repo
        self.session: Session = session

    def add_image(
            self,
            image_data: dict,
            schema: ImageSchemaAdd,
            faces_service: FaceService,
            faces_cloud_service: AbstractFaceCloudService
    ) -> dict:
        with self.session as s:
            image = self.image_repo(s).add_one(image_data)
            faces_data = faces_cloud_service().detected_faces(
                filename=image.filename,
                image_id=image.id
            )
            if faces_data:
                print(type(faces_data[0]['bounding_box']))
                faces_service(session=s).add_faces(faces_data=faces_data)
            return schema().dump(image)

    def get_image(self, image_data: dict, schema: ImageSchemaAdd) -> dict:
        with self.session as s:
            image = self.image_repo(s).get_one(image_data)
            return schema().dump(image)

    def delete_image(self, image_data: dict) -> dict:
        with self.session as s:
            count = self.image_repo(s).delete_one(image_data)
            return {'success': f'Number of images deleted: {count}'}
