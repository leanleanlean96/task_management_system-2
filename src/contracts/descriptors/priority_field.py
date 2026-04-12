from typing import Any

from ..exceptions.task_exceptions import InvalidTaskFieldValue

class PriorityField:
    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> int:
        return getattr(instance, self.private_name)
    
    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int) and not 0 < value < 6:
            raise InvalidTaskFieldValue(f"Can't assign {value} to {self.public_name}. Value must be an integer between 0 and 6")
        setattr(instance, self.private_name, value)