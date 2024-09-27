from flask import request, jsonify, make_response, Blueprint
from werkzeug.exceptions import RequestEntityTooLarge

from task_manager.db.db import db_session
from task_manager.repositories.faces import FaceRepository
from task_manager.repositories.images import ImageRepository
from task_manager.repositories.tasks import TaskRepository
from task_manager.schemas.images import ImageSchema, ImageResponseSchema
from task_manager.schemas.tasks import TaskResponseSchema, TaskSchema
from task_manager.services.file_operator import FileOperator
from task_manager.services.images import ImageService
from task_manager.app import auth
from task_manager.services.statistic import StatisticService
from task_manager.services.tevian import TevianFaceCloudService


images_bp = Blueprint('images_routes', __name__)


@images_bp.route('/images/<int:id>', methods=['GET'])
@auth.login_required
def get_image(id: int):
    try:
        with db_session() as s:
            repository = ImageRepository(s)
            image = ImageService(
                image_repo=repository,
                statistic_service=StatisticService(),
                file_operator=FileOperator(),
                session=s
            ).get_image(image_data={'id': id})
    except Exception:
        return make_response(
            jsonify({'error': 'Error get image'}),
            404
        )
    return jsonify(image)


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
        with db_session() as s:
            repository = ImageRepository(s)
            image = ImageService(
                image_repo=repository,
                statistic_service=StatisticService(),
                file_operator=FileOperator(),
                session=s
            ).add_image(
                image_data=image_data,
                file=image,
                faces_cloud_service=TevianFaceCloudService()
            )
        return jsonify(image)
    except TypeError:
        return make_response({'error': 'change file type'}, 400)
    except RequestEntityTooLarge:
        return make_response({'error': 'file is very large'}, 400)
    except Exception:
        return make_response(
            jsonify({'error': 'Error create image'}),
            500
        )


@images_bp.route('/images/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_image(id: int):
    try:
        with db_session() as s:
            repository = ImageRepository(s)
            response = ImageService(
                image_repo=repository,
                statistic_service=StatisticService(),
                file_operator=FileOperator(),
                session=s
            ).delete_image(image_data={'id': id})
    except:
        return make_response(
            jsonify({'error': 'Error delete image'}),
            404
        )
    return make_response(jsonify(response))
