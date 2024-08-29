from task_manager.utils.repository import AbstractRepository
from task_manager.schemas.tasks import TaskSchemaAdd
from task_manager.db.db import Session


class TaskService:
    def __init__(self,
                 task_repo: AbstractRepository,
                 session: Session
                 ):
        self.task_repo: AbstractRepository = task_repo
        self.session: Session = session

    def add_task(self,
                 task_data: dict,
                 schema: TaskSchemaAdd
                 ) -> dict:
        with self.session as s:
            task = self.task_repo(s).add_one(task_data)
            return schema().dump(task)

    def get_task(self,
                 task_data: dict,
                 schema: TaskSchemaAdd
                 ) -> dict:
        with self.session as s:
            task = self.task_repo(s).get_one(task_data)
            return schema().dump(task)

    def delete_task(self,
                    task_data: dict
                    ) -> dict:
        with self.session as s:
            count = self.task_repo(s).delete_one(task_data)
            return {'success': f'Number of tasks deleted: {count}'}
