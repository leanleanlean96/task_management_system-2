from typing import Any


class ShortIdField:
    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_name = name

    def __get__(self, instance: Any, owner: Any) -> str:
        short_id = instance.id.split("-")[0]
        instance.__dict__[self.public_name] = short_id
        return short_id
