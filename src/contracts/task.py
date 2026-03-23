import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Task:
    """Base class for Tasks"""
    id: str
    name: str
    description: str
    is_completed: bool
    creation_date: datetime
    completion_date: datetime | None

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        is_completed: bool,
        creation_date: datetime,
        completion_date: datetime | None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.is_completed = is_completed
        self.creation_date = creation_date
        self.completion_date = completion_date

    def __str__(self):
        return f"{'-' * 40}\nTask: {self.name}\ndescription: {self.description}\ncompletion status: {self.is_completed}\ncreated at: {self.creation_date}\ncompleted at: {self.completion_date if self.is_completed else 'Not completed'}\n{'-' * 40}"
