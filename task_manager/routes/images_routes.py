from flask import request, jsonify, make_response, Blueprint
from marshmallow import ValidationError
from task_manager.services.file_operator import FileOperator
from werkzeug.exceptions import RequestEntityTooLarge

from task_manager.services.images import ImageService
from task_manager.app import auth
from task_manager.schemas.images import ImageSchemaAdd


images_bp = Blueprint('images_routes', __name__)


@images_bp.route('/images/<int:id>', methods=['GET'])
@auth.login_required
def get_image(id: int):
    try:
        image = ImageService().get_image(image_data={'id': id})
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
        image_data = FileOperator().save(image, file_size)
        image_data['task_id'] = task_id
        image_data['filename']: filename
        image = ImageService().add_image(image_data=image_data)
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
        response = ImageService().delete_image({'id': id})
    except:
        return make_response(
            jsonify({'error': 'Error delete image'}),
            404
        )
    return make_response(jsonify(response))
