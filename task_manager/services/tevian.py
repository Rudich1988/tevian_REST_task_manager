from typing import Optional

import requests

from task_manager.utils.services import AbstractFaceCloudService
from task_manager.config.base import Config
from task_manager.exceptions.tevian_exceptions import TevianError
from task_manager.dto.faces import FaceDataDTO


class TevianFaceCloudService(AbstractFaceCloudService):
    def detected_faces(
            self,
            file,
            image_id
    ) -> list[Optional[FaceDataDTO]]:
        url = f"{Config.FACE_CLOUD_URL}/api/v1/detect"
        token = Config.FACE_ClOUD_TOKEN
        params = {
            "demographics": "true",
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'image/jpeg'
        }
        image_file = file.read()
        response = requests.post(
            url=url,
            headers=headers,
            data=image_file,
            params=params
        )
        if 'data' not in response.json():
            raise TevianError(
                message=response.json()['message'],
                status_code=response.json()['status_code']
            )
        faces_data = self.transform_data(response.json()['data'], image_id)
        return faces_data

    def transform_data(
            self,
            data,
            image_id
    ) -> list[Optional[FaceDataDTO]]:
        if not data:
            return []
        faces = []
        for face in data:
            face = FaceDataDTO(
                image_id=image_id,
                bounding_box=face['bbox'],
                age=face['demographics']['age']['mean'],
                gender=face['demographics']['gender']
            )
            faces.append(face)
        return faces
