from flask import jsonify, make_response, Blueprint

from task_manager.db.db import db_session
from task_manager.schemas.faces import FaceSchema
from task_manager.services.faces import FaceService
from task_manager.app import auth
from task_manager.repositories.faces import FaceRepository


faces_bp = Blueprint('faces_routes', __name__)


@faces_bp.route('/faces/<int:id>', methods=['GET'])
@auth.login_required
def get_face(id: int):
    try:
        with db_session() as s:
            face = FaceService(
                face_repo=FaceRepository(s),
                schema=FaceSchema()
            ).get_face(face_data={'id': id})
    except IndexError:
        return make_response(
            jsonify({'error': 'face not found'}),
            404
        )
    except Exception:
        return make_response(
            jsonify({'error': 'server error'}),
            500
        )
    return jsonify(face)
