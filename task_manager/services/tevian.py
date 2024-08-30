import requests

from task_manager.utils.services import AbstractFaceCloudService
from task_manager.config.base import Config


class TevianFaceCloudService(AbstractFaceCloudService):
    def detected_faces(self, filepath: str):
        url = f"{Config.FACE_CLOUD_URL}/api/v1/faces/detect"
        token = Config.FACE_ClOUD_TOKEN
        headers = {
            'Authorization': f'Bearer {token}'
        }
        with open(filepath, 'rb') as image_file:
            response = requests.post(
                url=url,
                files={'image': image_file},
                headers=headers
            )
        response.raise_for_status()
        return response.json()
