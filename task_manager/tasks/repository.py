from dataclasses import asdict

from sqlalchemy.orm import joinedload
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound

from task_manager.tasks.models import Task
from task_manager.utils.repository import SQLAlchemyRepository
from task_manager.tasks.dto import TaskDTO, TaskCreateDTO, TaskStatisticDTO
from task_manager.images.repository import ImageRepository
from task_manager.images.models import Image


class TaskRepository(SQLAlchemyRepository):
    model = Task

    def create_task_dto(self, task) -> TaskDTO:
        images = []
        if task.images:
            for image in task.images:
                images.append(
                    ImageRepository(
                        session=self.session
                    ).create_image_dto(image)
                )
        task_dto = TaskDTO(
            id=task.id,
            women_counter=task.women_counter,
            male_counter=task.male_counter,
            men_avg_age=task.men_avg_age,
            women_avg_age=task.women_avg_age,
            faces_counter=task.faces_counter,
            title=task.title,
            images=images
        )
        return task_dto

    def get_one(self, task_id: int) -> TaskDTO:
        query = (
            select(self.model)
            .where(self.model.id == task_id)
            .options(
                joinedload(self.model.images)
                .joinedload(Image.faces)
            )
        )
        task = self.session.execute(query).scalars().first()
        if not task:
            raise NoResultFound
        return self.create_task_dto(task)

    def add_one(self, task_data: TaskCreateDTO) -> TaskDTO:
        task = self.model(
            **asdict(task_data, dict_factory=dict)
        )
        task.images = []
        self.session.add(task)
        self.session.flush()
        return self.create_task_dto(task)

    def delete_one(self, task_id: int) -> None:
        stmt = delete(self.model).where(self.model.id == task_id)
        result = self.session.execute(stmt)
        if result.rowcount == 0:
            raise NoResultFound

    def update_one(
            self,
            task_id: int,
            fields: TaskStatisticDTO
    ) -> None:
        task = (self.session.query(self.model)
                .filter_by(id=task_id)
                .update(asdict(fields, dict_factory=dict))
                )
        self.session.flush()
