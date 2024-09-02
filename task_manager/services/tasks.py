from task_manager.db.db import db_session
from task_manager.schemas.tasks import TaskSchemaAdd, TaskSchemaResponse
from task_manager.repositories.tasks import TaskRepository


class TaskService:
    def __init__(
            self,
            session=db_session,
            task_repo=TaskRepository,
            schema=TaskSchemaAdd,
            response_schema=TaskSchemaResponse
    ):
        self.task_repo = task_repo
        self.session = session
        self.schema = schema()
        self.schema_response = response_schema()

    def add_task(self, task_data: dict) -> dict:
        with self.session() as s:
            task = self.task_repo(s).add_one(task_data)
            task = self.schema_response.dump(task)
        return task

    def get_task(self, task_data: dict) -> dict:
        with self.session() as s:
            task = self.task_repo(s).get_one(task_data)
            return self.schema_response.dump(task)

    def delete_task(self, task_data: dict) -> dict:
        with self.session() as s:
            count = self.task_repo(s).delete_one(task_data)
            return {'success': f'Number of tasks deleted: {count}'}
