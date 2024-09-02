from task_manager.db.db import db_session
from task_manager.schemas.tasks import TaskSchemaAdd
#from task_manager.db.db import Session
from task_manager.repositories.tasks import TaskRepository


class TaskService:
    def __init__(
            self,
            session=db_session,
            task_repo=TaskRepository,
            schema=TaskSchemaAdd
    ):
        self.task_repo = task_repo
        self.session = session
        self.schema = schema()

    def add_task(self, task_data: dict) -> dict:
        with self.session() as s:
            task = self.task_repo(s).add_one(task_data)
            task = self.schema.dump(task)
            #return self.schema.dump(task)
        return task

    def get_task(self, task_data: dict) -> dict:
        with self.session() as s:
            task = self.task_repo(s).get_one(task_data)
            return self.schema.dump(task)

    def delete_task(self, task_data: dict) -> dict:
        with self.session() as s:
            count = self.task_repo(s).delete_one(task_data)
            return {'success': f'Number of tasks deleted: {count}'}
