from dataclasses import asdict

from flask import request, jsonify, make_response, Blueprint, Response
from werkzeug.exceptions import RequestEntityTooLarge
from sqlalchemy.exc import IntegrityError, NoResultFound

from task_manager.db.db import db_session
from task_manager.images.repository import ImageRepository
from task_manager.tasks.repository import TaskRepository
from task_manager.images.schemas import ImageResponseSchema
from task_manager.images.file_operator import FileOperator
from task_manager.images.service import ImageService
from task_manager.app import auth
from task_manager.statistic.task_statistic import StatisticService
from task_manager.images.dto import ImageDataDTO
from task_manager.exceptions.tevian_exceptions import TevianError
from task_manager.exceptions.custom_exceptions import FileTypeError


images_bp = Blueprint('images_routes', __name__)


@images_bp.route('/images/<int:id>', methods=['GET'])
@auth.login_required
def get_image(id: int):
    try:
        with db_session() as s:
            repository = ImageRepository(s)
            image = ImageService(
                image_repo=repository
            ).get_image(image_id=id)
            image_data = ImageResponseSchema().load(
                asdict(image, dict_factory=dict)
            )
            return jsonify(image_data)
    except NoResultFound:
        return make_response(
            jsonify(
                {'error': 'image not found'}),
            404
        )
    except Exception:
        return make_response(
            jsonify(
                {'error': 'server error'}),
            500
        )


@images_bp.route('/images', methods=['POST'])
@auth.login_required
def create_image():
    try:
        image = request.files['file']
        task_id = request.form.get('task_id')
        filename = image.filename
        file_size = request.content_length
        image_data = FileOperator().check_file(image, file_size)
        image_data['task_id'] = task_id
        image_data['filename'] = filename
        image_data = ImageDataDTO(
            **image_data
        )
        with db_session() as s:
            image_repository = ImageRepository(s)
            image_data = ImageService(
                image_repo=image_repository
            ).add_image(image_data=image_data, file=image, session=s)
            image_data = ImageResponseSchema().load(
                asdict(image_data, dict_factory=dict)
            )
        FileOperator().save(image, image_data['filepath'])
        return jsonify(image_data)
    except IntegrityError:
        return make_response(
            jsonify({'error': 'incorrect task id'}),
            404
        )
    except TevianError as e:
        return make_response(
            jsonify({'error': e.message}),
            e.status_code
        )
    except FileTypeError as e:
        return make_response(
            jsonify({'error': e.message}),
            e.status_code
        )
    except RequestEntityTooLarge:
        return make_response(
            jsonify({'error': 'file is very large'}),
            400
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )


@images_bp.route('/images/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_image(id: int):
    try:
        with db_session() as s:
            image_service = ImageService(ImageRepository(s))
            image = image_service.get_image(image_id=id)
            faces = image.faces
            filepath = image.filepath
            if faces:
                StatisticService().decrement(
                    task_id=image.task_id,
                    faces_data=faces,
                    task_repo=TaskRepository(s)
                )
            FileOperator().delete(files=[filepath])
            image_service.delete_image(
                image_id=id
            )
            return Response(status=204)
    except NoResultFound:
        return make_response(
            jsonify({'error': 'image not found'}),
            404
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )
