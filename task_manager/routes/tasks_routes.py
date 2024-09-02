from flask import request, jsonify, make_response, Blueprint
from marshmallow import ValidationError

from task_manager.services.tasks import TaskService
from task_manager.db.db import Session
from task_manager.app import auth
from task_manager.schemas.tasks import TaskSchemaAdd


tasks_bp = Blueprint('tasks_routes', __name__)


@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
@auth.login_required
def get_task(id: int):
    try:
        task = TaskService().get_task(task_data={'id': id})
    except:
        return make_response(
            jsonify({'error': 'Error get task'}),
            404
        )
    return jsonify(task)


@tasks_bp.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    try:
        task_schema = TaskSchemaAdd()
        task_data = task_schema.load(request.json)
        task = TaskService().add_task(task_data=task_data)
    except ValidationError as error:
        return make_response({'error': error.messages}, 400)
    except Exception as e:
        print(e)
        return make_response(
            jsonify({'error': 'Error create task'}),
            404
        )
    return jsonify(task)


@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_task(id: int):
    try:
        response = TaskService().delete_task({'id': id})
    except:
        return make_response(
            jsonify({'error': 'Error delete task'}),
            404
        )
    return make_response(jsonify(response))
