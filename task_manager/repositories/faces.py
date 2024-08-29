from task_manager.models.faces import Face
from task_manager.utils.repository import SQLAlchemyRepository


class FaceRepository(SQLAlchemyRepository):
    model = Face
