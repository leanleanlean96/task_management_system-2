import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.contracts.task import Task
from src.contracts.exceptions.task_exceptions import TaskError


def parse_jsonl(path: Path) -> Iterator[tuple[int, dict[str, Any]]]:
    """Yield (line_number, parsed_dict) for each non-empty line of a JSONL file."""
    with path.open() as f:
        for line_num, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield line_num, json.loads(stripped)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON at line {line_num}: {e}")


@dataclass(frozen=True)
class JsonSource:
    """Reads Tasks from a JSONL file."""

    path: Path
    name: str = "JsonFile"

    def __post_init__(self) -> None:
        if self.path is None:
            raise ValueError("No path specified while creating JsonSource")

    def get_tasks(self) -> Iterable[Task]:
        for line_num, task in parse_jsonl(self.path):
            try:
                yield Task.from_dict(data=task)
            except TaskError as e:
                print(f"Skipping task at line {line_num}: {e}")