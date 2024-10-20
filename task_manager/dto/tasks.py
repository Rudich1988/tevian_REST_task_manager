from dataclasses import dataclass
from typing import Optional

from task_manager.dto.images import ImageDTO


@dataclass
class TaskDTO:
    id: int
    faces_counter: int
    women_counter: int
    male_counter: int
    men_avg_age: int
    women_avg_age: int
    title: str
    images: list[Optional[ImageDTO]]


@dataclass
class TaskCreateDTO:
    title: str
    faces_counter: int
    women_counter: int
    male_counter: int
    men_avg_age: float
    women_avg_age: float


@dataclass
class TaskStatisticDTO:
    faces_counter: int
    women_counter: int
    male_counter: int
    men_avg_age: float
    women_avg_age: float