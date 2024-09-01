import json

import requests

from task_manager.utils.services import AbstractFaceCloudService
from task_manager.config.base import Config


class TevianFaceCloudService(AbstractFaceCloudService):
    def detected_faces(self, filename: str, image_id):
        url = f"{Config.FACE_CLOUD_URL}/api/v1/detect"
        token = Config.FACE_ClOUD_TOKEN
        params = {
            "demographics": "true",
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'image/jpeg'
        }
        with open(filename, 'rb') as image_file:
            response = requests.post(
                url=url,
                headers=headers,
                data=image_file,
                params=params
            )
        faces_data = self.transform_data(response.json()['data'], image_id)
        return faces_data

    def transform_data(self, data, image_id):
        if not data:
            return []
        faces = []
        for face in data:
            face_data = {}
            face_data['image_id'] = image_id
            face_data['bounding_box'] = face['bbox']#json.dumps(face['bbox'])
            face_data['age'] = face['demographics']['age']['mean']
            face_data['gender'] = face['demographics']['gender']
            faces.append(face_data)
        return faces
