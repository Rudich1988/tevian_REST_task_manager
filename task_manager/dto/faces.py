from dataclasses import dataclass


@dataclass
class FaceDTO:
    bounding_box: dict
    gender: str
    age: float


@dataclass
class FaceResponseDTO:
    id: int
    bounding_box: dict
    gender: str
    age: float
    image_id: int


@dataclass
class FaceDataDTO:
    bounding_box: dict
    gender: str
    age: float
    image_id: int
