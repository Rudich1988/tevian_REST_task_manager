from task_manager.repositories.images import ImageRepository
from task_manager.repositories.tasks import TaskRepository
from task_manager.services.file_operator import FileOperator
from task_manager.dto.tasks import TaskDTO, TaskCreateDTO
from task_manager.db.db import Session


class TaskService:
    def __init__(
            self,
            task_repo: TaskRepository
    ):
        self.task_repo = task_repo

    def add_task(self, task_data: TaskCreateDTO) -> TaskDTO:
        return self.task_repo.add_one(task_data=task_data)

    def get_task(self, task_id: int) -> TaskDTO:
        task = self.task_repo.get_one(task_id=task_id)
        return task

    def delete_task(self,
                    task_id: int,
                    file_operator: FileOperator,
                    session: Session
                    ) -> None:
        files = ImageRepository(
            session=session
        ).get_files(task_id=task_id)
        if files:
            file_operator.delete(files=files)
        self.task_repo.delete_one(task_id=task_id)
