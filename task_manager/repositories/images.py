from task_manager.models.images import Image
from task_manager.utils.repository import SQLAlchemyRepository


class ImageRepository(SQLAlchemyRepository):
    model = Image
