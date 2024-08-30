from flask import request, jsonify, make_response, Blueprint

from task_manager.services.tasks import TaskService
from task_manager.repositories.tasks import TaskRepository
from task_manager.schemas.tasks import TaskSchemaAdd
from task_manager.db.db import Session


tasks_bp = Blueprint('tasks_routes', __name__)


@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(
        id: int,
        task_service=TaskService,
        task_repo=TaskRepository,
        task_schema=TaskSchemaAdd,
        session=Session
):
    try:
        task = task_service(
            task_repo=task_repo,
            session=session()).get_task(
            task_data={'id': id},
            schema=task_schema
        )
    except:
        return make_response(
            jsonify({'error': 'Error get task'}),
            404
        )
    return jsonify(task)


@tasks_bp.route('/tasks', methods=['POST'])
def create_task(
        task_service=TaskService,
        task_repo=TaskRepository,
        task_schema=TaskSchemaAdd,
        session=Session
):
    try:
        task_data = request.json
        task = task_service(
            task_repo=task_repo,
            session=session()).add_task(
            task_data=task_data,
            schema=task_schema
        )
    except:
        return make_response(
            jsonify({'error': 'Error create task'}),
            404
        )
    return jsonify(task)


@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(
        id: int,
        task_service=TaskService,
        task_repo=TaskRepository,
        session=Session
):
    try:
        response = task_service(
            task_repo=task_repo,
            session=session()).delete_task({'id': id})
    except:
        return make_response(
            jsonify({'error': 'Error delete task'}),
            404
        )
    return make_response(jsonify(response))
