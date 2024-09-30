from flask import request, jsonify, make_response, Blueprint
from marshmallow import ValidationError

from task_manager.services.file_operator import FileOperator
from task_manager.services.tasks import TaskService
from task_manager.app import auth
from task_manager.schemas.tasks import TaskSchema, TaskResponseSchema
from task_manager.db.db import db_session
from task_manager.repositories.tasks import TaskRepository


tasks_bp = Blueprint('tasks_routes', __name__)


@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
@auth.login_required
def get_task(id: int):
    try:
        with db_session() as s:
            repository = TaskRepository(s)
            task = TaskService(
                task_repo=repository
            ).get_task(task_data={'id': id})
    except IndexError:
        return make_response(
            jsonify({'error': 'task not found'}),
            404
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )
    return jsonify(task)


@tasks_bp.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    try:
        with db_session() as s:
            task_schema = TaskSchema()
            task_data = task_schema.load(request.json)
            repository = TaskRepository(s)
            task = TaskService(
                task_repo=repository
            ).add_task(task_data=task_data)
    except ValidationError as error:
        return make_response({'error': error.messages}, 400)
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )
    return jsonify(task)


@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_task(id: int):
    try:
        with db_session() as s:
            repository = TaskRepository(s)
            response = TaskService(
                task_repo=repository
            ).delete_task(
                task_data={'id': id},
                file_operator=FileOperator()
            )
    except IndexError:
        return make_response(
            jsonify({'error': 'task not found'}, 404)
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )
    return make_response(jsonify(response))
