import requests

from task_manager.utils.services import AbstractFaceCloudService
from task_manager.config.base import Config


class TevianFaceCloudService(AbstractFaceCloudService):
    def detected_faces(self, filename: str):
        try:
            url = f"{Config.FACE_CLOUD_URL}/api/v1/detect"
            token = Config.FACE_ClOUD_TOKEN
            headers = {
                'Authorization': f'Bearer {token}',
            }
            with open(filename, 'rb') as image_file:
                files = {'file': ('image.jpg', image_file, 'image/jpeg')}
                response = requests.post(
                    url=url,
                    files=files,
                    headers=headers
                )
            #response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            try:
                # Печать тела ответа для диагностики
                print("Response body:", response.json())
            except ValueError:
                print("Response body is not JSON.")
        except Exception as err:
            print(f"Other error occurred: {err}")
