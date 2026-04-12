from typing import Any

from ..exceptions.task_exceptions import InvalidTaskFieldValue


class StringField:
    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> str:
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: str) -> None:
        if not value or not isinstance(value, str):
            raise InvalidTaskFieldValue(
                f"Can't assign {value} to {self.public_name}. {value} is an invalid string"
            )
        setattr(instance, self.private_name, value)
