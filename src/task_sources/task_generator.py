import random
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable
from uuid import uuid4

from src.contracts.task import Task

"""
    self.id = id
    self.name = name
    self.description = description
    self.is_completed = is_completed
    self.creation_date = creation_date
    self.completion_date = completion_date
"""


@dataclass()
class TaskGenerator:
    """TaskGenerator class for creating random Tasks"""
    name: str = "TaskGenerator"

    def __init__(
        self,
        name_list: list[str],
        description_list: list[str],
        creation_date_list: list[datetime],
        completion_date_list: list[datetime],
    ) -> None:
        self.name_list = name_list
        self.description_list = description_list
        self.creation_date_list = creation_date_list
        self.completion_date_list = completion_date_list

    def get_tasks(self) -> Iterable[Task]:
        random.seed()
        for i in range(random.randint(1, 33)):
            id = str(uuid4())
            name = random.choice(self.name_list)
            desc = random.choice(self.description_list)
            is_completed = random.choice([True, False])
            cr_date = random.choice(self.creation_date_list)
            completion_date = (
                None if not is_completed else random.choice(self.completion_date_list)
            )
            yield Task(id, name, desc, is_completed, cr_date, completion_date)
