import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.contracts.task import Task


def parse_json_file(path: Path) -> list[dict[str, Any]]:
    parsed_tasks = []
    with path.open() as json_file:
        for line_num, line in enumerate(json_file):
            if not line.strip():
                continue
            try:
                parsed_tasks.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return parsed_tasks


@dataclass(frozen=True)
class JsonSource:
    """Reads Tasks from Path/to.jsonl"""
    path: Path
    name: str = "Jsonfile"

    @staticmethod
    def create(path: Path):
        if path is None:
            raise ValueError("Path can't be empty")
        return JsonSource(path=path)

    def get_tasks(self) -> Iterable[Task]:
        for task_dict in parse_json_file(self.path):
            try:
                task_id = task_dict["id"]
                task_name = task_dict["name"]
                task_desc = task_dict["description"]
                is_completed = task_dict["is_completed"]
                creation_date = task_dict["creation_date"]
                completion_date = task_dict["completion_date"]
                yield Task(
                    id=task_id,
                    name=task_name,
                    description=task_desc,
                    is_completed=is_completed,
                    creation_date=creation_date,
                    completion_date=completion_date,
                )
            except IndexError as e:
                print(f"An error occured: {e}")
