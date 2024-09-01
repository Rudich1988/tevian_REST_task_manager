from task_manager.models.tasks import Task
from task_manager.utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task

    def update_one(self, obj, data):
        for key, value in data.items():
            if key == 'faces_counter':
                obj.faces_counter = value
            if key == 'women_counter':
                obj.women_counter = value
            if key == 'male_counter':
                obj.male_counter = value
            if key == 'men_avg_age':
                obj.men_avg_age = value
            if key == 'women_avg_age':
                obj.women_avg_age = value
        self.session.commit()


