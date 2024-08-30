from flask import request, jsonify, make_response, Blueprint

from task_manager.services.images import ImageService
from task_manager.repositories.images import ImageRepository
from task_manager.schemas.images import ImageSchemaAdd
from task_manager.db.db import Session


images_bp = Blueprint('images_routes', __name__)


@images_bp.route('/images/<int:id>', methods=['GET'])
def get_image(
        id: int,
        image_service=ImageService,
        image_repo=ImageRepository,
        image_schema=ImageSchemaAdd,
        session=Session
):
    try:
        image = image_service(
            image_repo=image_repo,
            session=session()).get_image(
            image_data={'id': id},
            schema=image_schema
        )
    except:
        return make_response(
            jsonify({'error': 'Error get image'}),
            404
        )
    return jsonify(image)


@images_bp.route('/images', methods=['POST'])
def create_image(
        image_service=ImageService,
        image_repo=ImageRepository,
        image_schema=ImageSchemaAdd,
        session=Session
):
    try:
        image_data = request.json
        image = image_service(
            image_repo=image_repo,
            session=session()).add_image(
            image_data=image_data,
            schema=image_schema
        )
    except:
        return make_response(
            jsonify({'error': 'Error create image'}),
            404
        )
    return jsonify(image)


@images_bp.route('/images/<int:id>', methods=['DELETE'])
def delete_image(
        id: int,
        image_service=ImageService,
        image_repo=ImageRepository,
        session=Session
):
    try:
        response = image_service(
            image_repo=image_repo,
            session=session()).delete_image({'id': id})
    except:
        return make_response(
            jsonify({'error': 'Error delete image'}),
            404
        )
    return make_response(jsonify(response))
