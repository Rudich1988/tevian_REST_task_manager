from dataclasses import dataclass
from typing import Optional

from task_manager.dto.faces import FaceDTO


#@dataclass
#class ImageDTO:
 #   filename: str
  #  faces: list[Optional[FaceDTO]]


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
