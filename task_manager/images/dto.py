from dataclasses import dataclass
from typing import Optional

from task_manager.faces.dto import FaceDTO


@dataclass
class ImageDTO:
    id: int
    filename: str
    unique_filename: str
    filepath: str
    task_id: int
    faces: list[Optional[FaceDTO]]


@dataclass
class ImageDataDTO:
    filepath: str
    unique_filename: str
    task_id: int
    filename: str
