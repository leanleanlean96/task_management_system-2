from typing import Any

from .stdin import StdinSource
from .task_generator import TaskGenerator
from .task_json import JsonSource

SOURCES: dict[str, Any] = {
    "stdin": StdinSource,
    "json": JsonSource,
    "generator": TaskGenerator,
}
