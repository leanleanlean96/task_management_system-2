from datetime import datetime, timezone
from typing import Literal, Optional, Self
from uuid import uuid4

from .descriptors.datetime_field import DateField
from .descriptors.id_field import IdField
from .descriptors.str_field import StringField
from .descriptors.priority_field import PriorityField
from .descriptors.short_id import ShortIdField

from .exceptions.task_exceptions import InvalidTaskData, AccessPermitted, InvalidTaskFieldValue

class Task:
    """Base class for Tasks"""
    id: str = IdField()
    short_id: str = ShortIdField()
    title: str = StringField()
    description: str = StringField()
    priority: int = PriorityField()
    creation_date: datetime = DateField()
    completion_date: datetime | None = DateField()

    def __init__(
        self,
        *,
        id: str,
        title: str,
        description: str = "",
        priority: int,
        creation_date: datetime,
        completion_date: Optional[datetime] = None,
    ) -> None:
        
        if creation_date is None:
            creation_date = datetime.now(timezone.utc)
        if completion_date is not None and creation_date > completion_date:
            raise InvalidTaskData("Task is completed before it is created")
        
        self.id = id
        self.title = title
        self.description = description
        self.priority= priority
        self.creation_date = creation_date
        self.completion_date = completion_date

    @classmethod
    def from_dict(cls, *, data: dict) -> Self:
        try:
            completion_raw = data.get("completion_date")
            return cls(
                id=data["id"],
                title=data["title"],
                description=data.get("description", ""),
                priority=data["priority"],
                creation_date=datetime.fromisoformat(data["creation_date"]),
                completion_date=(
                    datetime.fromisoformat(completion_raw) if completion_raw else None
                ),
            )
        except KeyError as e:
            raise InvalidTaskData(f"Missing required field: {e.args[0]}") from e
        except ValueError as e:
            raise InvalidTaskFieldValue(f"Invalid field value: {e}") from e

    @classmethod
    def create(
        cls,
        *,
        title: str,
        description: str = "",
        priority: int = 5,
        creation_date: Optional[datetime] = None,
        completion_date: Optional[datetime] = None,
    ) -> Self:
        
        return cls(
            id=str(uuid4()),
            title=title,
            description=description,
            priority=priority,
            creation_date=creation_date,
            completion_date=completion_date,
        )

    def complete(self, comp_date: Optional[datetime] = None) -> None:
        if self.is_completed == "Completed":
            raise AccessPermitted("Task is already completed")
        if comp_date is None:
            comp_date = datetime.now(timezone.utc)
        if comp_date < self.creation_date:
            raise InvalidTaskData("completion_date can't be before creation_date")
        self.completion_date = comp_date
    
    @property
    def is_completed(self) -> str:
        return "Completed" if self.completion_date is not None else "Not Completed"

    def __str__(self) -> str:
        return (
            f"{'-' * 40}\n"
            f"Task: {self.title}\n"
            f"short_id: {self.short_id}\n"
            f"description: {self.description}\n"
            f"status: {self.is_completed}\n"
            f"priority: {self.priority}\n"
            f"created at: {self.creation_date}\n"
            f"completed at: {self.completion_date}\n"
            f"{'-' * 40}"
        )