from flask import jsonify, make_response, Blueprint

from task_manager.services.faces import FaceService
from task_manager.app import auth


faces_bp = Blueprint('faces_routes', __name__)


@faces_bp.route('/faces/<int:id>', methods=['GET'])
@auth.login_required
def get_face(id: int):
    try:
        face = FaceService().get_face(face_data={'id': id})
    except Exception:
        return make_response(
            jsonify({'error': 'Error get image'}),
            404
        )
    return jsonify(face)
