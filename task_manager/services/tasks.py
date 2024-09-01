from task_manager.utils.repository import AbstractRepository
from task_manager.schemas.tasks import TaskSchemaAdd
from task_manager.db.db import Session
from task_manager.models.tasks import Task
from task_manager.repositories.tasks import TaskRepository


class TaskService:
    def __init__(self, session: Session, task_repo=TaskRepository):
        self.task_repo: AbstractRepository = task_repo
        self.session: Session = session

    def add_task(self, task_data: dict, schema=TaskSchemaAdd) -> dict:
        with self.session as s:
            task = self.task_repo(s).add_one(task_data)
            return schema().dump(task)

    def get_task(self, task_data: dict, schema=TaskSchemaAdd) -> dict:
        with self.session as s:
            task = self.task_repo(s).get_one(task_data)
            return schema().dump(task)

    def delete_task(self, task_data: dict) -> dict:
        with self.session as s:
            count = self.task_repo(s).delete_one(task_data)
            return {'success': f'Number of tasks deleted: {count}'}

    def change_statistic(
            self,
            task: Task,
            data,
            operator: str,
            schema=TaskSchemaAdd):
        task = schema().dump(task)
        men_quantity = 0
        men_age = 0
        women_quantity = 0
        women_age = 0
        if operator == '+':
            task['faces_counter'] += len(data)
            for face_data in data:
                for key, value in face_data.items():
                    if key == 'gender':
                        if face_data[key] == 'female':
                            women_quantity += 1
                            women_age += face_data['age']
                        else:
                            men_quantity += 1
                            men_age += face_data['age']
            task['women_counter'] += women_quantity
            task['male_counter'] += men_quantity
            if men_quantity > 0:
                if task['men_avg_age'] == 0:
                    task['men_avg_age'] = men_age / men_quantity
                else:
                    task['men_avg_age'] = (task['men_avg_age'] + (men_age / men_quantity)) / 2
            if women_quantity > 0:
                if task['women_avg_age'] == 0:
                    task['women_avg_age'] = women_age / women_quantity
                else:
                    task['women_avg_age'] = (task['women_avg_age'] + (women_age / women_quantity)) / 2
            return task
        for face_data in data:
            for key, value in face_data.items():
                task['faces_counter'] -= 1
                if key == 'gender':
                    if face_data[key] == 'female':
                        women_quantity += 1
                        women_age += face_data['age']
                    else:
                        men_quantity += 1
                        men_age += face_data['age']
        remaining_count = task['women_counter'] - women_quantity
        total_age = task['women_counter'] * task['men_avg_age']
        remaining_age = total_age - women_age
        if remaining_count > 0:
            task['woman_avg_age'] = remaining_age / remaining_count
        else:
            task['woman_avg_age'] = 0
        task['women_counter'] += women_quantity

        remaining_count = task['male_counter'] - men_quantity
        total_age = task['male_counter'] * task['men_avg_age']
        remaining_age = total_age - men_age
        if remaining_count > 0:
            task['men_avg_age'] = remaining_age / remaining_count
        else:
            task['men_avg_age'] = 0
        task['men_counter'] += women_quantity
        return task
