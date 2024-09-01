import json

from flask import request, jsonify, make_response, Blueprint

from task_manager.services.faces import FaceService
from task_manager.repositories.faces import FaceRepository
from task_manager.schemas.faces import FaceSchema
from task_manager.db.db import Session
from task_manager.app import auth


faces_bp = Blueprint('faces_routes', __name__)


@faces_bp.route('/faces/<int:id>', methods=['GET'])
@auth.login_required
def get_face(
        id: int,
        face_service=FaceService,
        face_repo=FaceRepository,
        face_schema=FaceSchema,
        session=Session
):
    try:
        face = face_service(
            face_repo=face_repo,
            session=session()).get_face(
            face_data={'id': id},
            schema=face_schema
        )
    except:
        return make_response(
            jsonify({'error': 'Error get image'}),
            404
        )
    return jsonify(face)


@faces_bp.route('/faces', methods=['POST'])
@auth.login_required
def create_face(
        face_service=FaceService,
        face_repo=FaceRepository,
        face_schema=FaceSchema,
        session=Session
):
    try:
        face_data = request.json
        face_data['bounding_box'] = json.dumps(face_data['bounding_box'])
        face = face_service(
            face_repo=face_repo,
            session=session()).add_face(
            face_data=face_data,
            schema=face_schema)
    except:
        return make_response(
            jsonify({'error': 'Error create task'}),
            404
        )
    return jsonify(face)
