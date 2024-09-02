from flask import request, jsonify, make_response, Blueprint
from marshmallow import ValidationError

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
        image_schema = ImageSchemaAdd()
        image_data = image_schema.load(request.json)
        image = ImageService().add_image(image_data=image_data)
    except ValidationError as error:
        return make_response({'error': error.messages}, 400)
    except Exception:
        return make_response(
            jsonify({'error': 'Error create image'}),
            500
        )
    return jsonify(image)


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
