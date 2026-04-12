from typing import Any
from uuid import UUID

from ..exceptions.task_exceptions import AccessPermitted, InvalidTaskFieldValue


class IdField:
    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: type | None = None) -> str:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if self.private_name in instance.__dict__:
            raise AccessPermitted(f"{self.public_name} is immutable")
        if not isinstance(value, str):
            raise InvalidTaskFieldValue(
                f"{self.public_name} must be str, got {type(value).__name__}"
            )
        try:
            UUID(value)
        except ValueError as e:
            raise InvalidTaskFieldValue(
                f"{self.public_name} must be a valid UUID, got {value}"
            ) from e
        instance.__dict__[self.private_name] = value

    def __delete__(self, instance: Any) -> None:
        raise AccessPermitted(f"{self.public_name} cannot be deleted")
