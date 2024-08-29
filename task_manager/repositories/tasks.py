from task_manager.models.tasks import Task
from task_manager.utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task
