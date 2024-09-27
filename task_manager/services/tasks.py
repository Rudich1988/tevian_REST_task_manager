from task_manager.schemas.tasks import TaskResponseSchema
from task_manager.repositories.tasks import TaskRepository
from task_manager.services.file_operator import FileOperator


class TaskService:
    def __init__(
            self,
            task_repo: TaskRepository
    ):
        self.task_repo = task_repo

    def add_task(self, task_data: dict) -> dict:
        task = self.task_repo.add_one(task_data)
        return TaskResponseSchema().dump(task)
        #return task

    def get_task(self, task_data: dict) -> dict:
        task = self.task_repo.get_one(task_data)
        return TaskResponseSchema().dump(task)

    def delete_task(self,
                    task_data: dict,
                    file_operator: FileOperator
                    ) -> dict:
        images = self.task_repo.get_one(task_data).images
        filepathes = [image.filepath for image in images]
        file_operator.delete(filepathes=filepathes)
        count = self.task_repo.delete_one(task_data)
        return {'success': f'Number of tasks deleted: {count}'}
