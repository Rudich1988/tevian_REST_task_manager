from abc import ABC, abstractmethod


class AbstractFaceCloudService(ABC):
    @abstractmethod
    def detected_faces(self, filename: str, image_id):
        raise NotImplementedError

    @abstractmethod
    def transform_data(self, data, image_id):
        raise NotImplementedError