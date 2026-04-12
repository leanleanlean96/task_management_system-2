import random
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable
from uuid import uuid4

from src.contracts.task import Task

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
            name = random.choice(self.name_list)
            desc = random.choice(self.description_list)
            priority = random.randint(1, 5)
            cr_date = random.choice(self.creation_date_list)
            completion_date = random.choice(self.completion_date_list)
            yield Task.create(
                title=name,
                description=desc,
                priority=priority,
                creation_date=cr_date,
                completion_date=completion_date,
            )
