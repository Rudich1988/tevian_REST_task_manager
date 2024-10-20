from dataclasses import asdict

from flask import request, jsonify, make_response, Blueprint, Response
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from task_manager.services.file_operator import FileOperator
from task_manager.services.tasks import TaskService
from task_manager.app import auth
from task_manager.schemas.tasks import TaskSchema, TaskResponseSchema
from task_manager.db.db import db_session
from task_manager.repositories.tasks import TaskRepository
from task_manager.dto.tasks import TaskCreateDTO


tasks_bp = Blueprint('tasks_routes', __name__)


@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
@auth.login_required
def get_task(id: int):
    try:
        with db_session() as s:
            repository = TaskRepository(s)
            task = TaskService(
                task_repo=repository
            ).get_task(task_id=id)
            task_data = TaskSchema().load(
                asdict(task, dict_factory=dict)
            )
            return jsonify(task_data)
    except NoResultFound:
        return make_response(
            jsonify({'error': 'task not found'}),
            404
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )


@tasks_bp.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    try:
        with db_session() as s:
            task_schema = TaskSchema()
            task_data = TaskCreateDTO(
                **task_schema.load(request.json)
            )
            repository = TaskRepository(s)
            task = TaskService(
                task_repo=repository
            ).add_task(task_data=task_data)
            task_data = TaskResponseSchema().load(
                asdict(task, dict_factory=dict)
            )
            return jsonify(task_data)
    except ValidationError as error:
        return make_response(
            jsonify({'error': error.messages}),
            400
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )


@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_task(id: int):
    try:
        with db_session() as s:
            repository = TaskRepository(s)
            TaskService(
                task_repo=repository
            ).delete_task(
                task_id=id,
                file_operator=FileOperator(),
                session=s
            )
            return Response(status=204)
    except NoResultFound:
        return make_response(
            jsonify({'error': 'task not found'}),
            404
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )
