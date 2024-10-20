from task_manager.dto.tasks import TaskDTO, TaskStatisticDTO
from task_manager.repositories.tasks import TaskRepository


class StatisticService:
    def increment(
            self,
            faces_data: list,
            task_id: int,
            task_repo: TaskRepository
    ):
        task = task_repo.get_one(task_id=task_id)
        men_quantity = 0
        men_age = 0
        women_quantity = 0
        women_age = 0
        task.faces_counter += len(faces_data)
        for face_data in faces_data:
            if face_data.gender == 'female':
                women_quantity += 1
                women_age += face_data.age
            else:
                men_quantity += 1
                men_age += face_data.age
        task.women_counter += women_quantity
        task.male_counter += men_quantity
        if men_quantity > 0:
            if task.men_avg_age == 0:
                task.men_avg_age = men_age / men_quantity
            else:
                task.men_avg_age = (task.men_avg_age + \
                                       (men_age / men_quantity)) / 2
        if women_quantity > 0:
            if task.women_avg_age == 0:
                task.women_avg_age = women_age / women_quantity
            else:
                task.women_avg_age = (task.women_avg_age + \
                                         (women_age / women_quantity)) / 2
        return self.update_statistic(task, task_repo)

    def decrement(
            self,
            task_id: int,
            faces_data: list,
            task_repo: TaskRepository
    ):
        task = task_repo.get_one(task_id=task_id)
        men_quantity = 0
        men_age = 0
        women_quantity = 0
        women_age = 0
        task.faces_counter -= len(faces_data)
        for face_data in faces_data:
            if face_data.gender == 'female':
                women_quantity += 1
                women_age += face_data.age
            else:
                men_quantity += 1
                men_age += face_data.age
        remaining_count = task.women_counter - women_quantity
        total_age = task.women_counter * task.women_avg_age
        remaining_age = total_age - women_age
        if remaining_count > 0:
            task.woman_avg_age = remaining_age / remaining_count
        else:
            task.women_avg_age = 0
        task.women_counter -= women_quantity
        remaining_count = task.male_counter - men_quantity
        total_age = task.male_counter * task.men_avg_age
        remaining_age = total_age - men_age
        if remaining_count > 0:
            task.men_avg_age = remaining_age / remaining_count
        else:
            task.men_avg_age = 0
        task.male_counter -= men_quantity
        return self.update_statistic(task, task_repo)

    def update_statistic(
            self,
            task: TaskDTO,
            task_repo: TaskRepository
    ) -> None:
        task_data = TaskStatisticDTO(
            faces_counter=task.faces_counter,
            male_counter=task.male_counter,
            women_counter=task.women_counter,
            men_avg_age=task.men_avg_age,
            women_avg_age=task.women_avg_age
        )
        task_repo.update_one(
            task_id=task.id,
            fields=task_data
        )
