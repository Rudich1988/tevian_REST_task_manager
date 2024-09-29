from flask import request, jsonify, make_response, Blueprint
from werkzeug.exceptions import RequestEntityTooLarge
from sqlalchemy.exc import IntegrityError

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
from task_manager.exceptions.custom_exceptions import FileTypeError
from task_manager.exceptions.tevian_exceptions import TevianError


images_bp = Blueprint('images_routes', __name__)


@images_bp.route('/images/<int:id>', methods=['GET'])
@auth.login_required
def get_image(id: int):
    try:
        with db_session() as s:
            repository = ImageRepository(s)
            image = ImageService(
                image_repo=repository
            ).get_image(image_data={'id': id})
    except IndexError:
        return make_response({"error": "image not found"}, 404)
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
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
            image_repository = ImageRepository(s)
            image_data = ImageService(
                image_repo=image_repository
            ).add_image(image_data=image_data)
            faces_data = TevianFaceCloudService().detected_faces(
                file=image,
                image_id=image_data['id'])
            if faces_data:
                FaceRepository(s).add_objects(data=faces_data)
                StatisticService().increment(
                    task_id=image_data['task_id'],
                    data=faces_data,
                    task_repo=TaskRepository(s)
                )
            image_data = ImageService(
                image_repo=image_repository
            ).get_image(
                image_data={'id': image_data['id']}
            )
        FileOperator().save(image, image_data['filepath'])
        return jsonify(image_data)
    except IntegrityError:
        return make_response({'error': 'incorrect task id'}, 404)
    except TevianError as e:
        return make_response({'error': e.message}, e.status_code)
    except FileTypeError as e:
        return make_response({'error': e.message}, e.status_code)
    except RequestEntityTooLarge:
        return make_response({'error': 'file is very large'}, 400)
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
            image = image_service.get_image({'id': id})
            faces = image['faces']
            filepath = image['filepath']
            if faces:
                StatisticService().decrement(
                    task_id=image['task_id'],
                    data=faces,
                    task_repo=TaskRepository(s)
                )
            FileOperator().delete(files=[filepath])
            response = image_service.delete_image(
                image_data={'id': id}
            )
    except IndexError:
        return make_response(
            jsonify({'error': 'image not found'}, 404)
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )
    return make_response(jsonify(response))
