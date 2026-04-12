from datetime import datetime
from typing import Any, Optional

from ..exceptions.task_exceptions import InvalidTaskFieldValue

class DateField:
    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> Optional[datetime]:
        return getattr(instance, self.private_name)
    
    def __set__(self, instance: Any, value: datetime) -> None:
        if not isinstance(value, datetime) and value is not None:
            raise InvalidTaskFieldValue(f"Can't assign {value} to {self.public_name}. Value must be a datetime object or None")
        setattr(instance, self.private_name, value)