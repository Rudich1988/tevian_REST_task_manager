from task_manager.utils.repository import AbstractRepository
from task_manager.schemas.images import ImageSchemaAdd
from task_manager.db.db import Session


class ImageService:
    def __init__(self,
                 image_repo: AbstractRepository,
                 session: Session
                 ):
        self.image_repo: AbstractRepository = image_repo
        self.session: Session = session

    def add_image(self,
                 image_data: dict,
                 schema: ImageSchemaAdd
                 ) -> dict:
        with self.session as s:
            image = self.image_repo(s).add_one(image_data)
            return schema().dump(image)

    def get_image(self,
                 image_data: dict,
                 schema: ImageSchemaAdd) -> dict:
        with self.session as s:
            image = self.image_repo(s).get_one(image_data)
            return schema().dump(image)

    def delete_image(self,
                    image_data: dict
                    ) -> dict:
        with self.session as s:
            count = self.image_repo(s).delete_one(image_data)
            return {'success': f'Number of images deleted: {count}'}
