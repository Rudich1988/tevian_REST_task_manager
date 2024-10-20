from dataclasses import asdict

from flask import jsonify, make_response, Blueprint
from sqlalchemy.exc import NoResultFound

from task_manager.db.db import db_session
from task_manager.faces.schemas import FaceResponseSchema
from task_manager.faces.service import FaceService
from task_manager.app import auth
from task_manager.faces.repository import FaceRepository


faces_bp = Blueprint('faces_routes', __name__)


@faces_bp.route('/faces/<int:id>', methods=['GET'])
@auth.login_required
def get_face(id: int):
    try:
        with db_session() as s:
            face = FaceService(
                face_repo=FaceRepository(s)
            ).get_face(face_id=id)
            face = FaceResponseSchema().load(
                asdict(face, dict_factory=dict)
            )
            return jsonify(face)
    except NoResultFound:
        return make_response(
            jsonify({'error': 'face not found'}),
            404
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )
