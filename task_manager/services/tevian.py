import requests

from task_manager.utils.services import AbstractFaceCloudService
from task_manager.config.base import Config


class TevianFaceCloudService(AbstractFaceCloudService):
    def detected_faces(self, filename: str):
        url = f"{Config.FACE_CLOUD_URL}/api/v1/detect"
        token = Config.FACE_ClOUD_TOKEN
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'image/jpeg'
        }
        with open(filename, 'rb') as image_file:
            response = requests.post(
                url=url,
                headers=headers,
                data=image_file
            )
        faces_data = response.json()['data']
        return response.json()
