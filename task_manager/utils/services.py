from abc import ABC, abstractmethod


class AbstractFaceCloudService(ABC):
    @abstractmethod
    def detected_faces(self, filename: str):
        raise NotImplementedError
