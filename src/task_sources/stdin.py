import sys
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import TextIO

from src.contracts.task import Task
from src.contracts.exceptions.task_exceptions import TaskError, InvalidTaskData


@dataclass(frozen=True)
class StdinSource:
    """Reads new Tasks from a text stream (default is stdin).

    Expected format per line, ';'-separated:
        title;description;priority[;creation_date[;completion_date]]
    """

    stream: TextIO = sys.stdin
    name: str = "stdin"

    def get_tasks(self) -> Iterable[Task]:
        for line_num, line in enumerate(self.stream, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield _parse_and_create(stripped)
            except TaskError as e:
                print(f"Skipping task at line {line_num}: {e}")


def _parse_and_create(line: str) -> Task:
    try:
        fields = [f.strip() for f in line.split(";")]
        title = fields[0]
        desc = fields[1]
        priority = int(fields[2])
        creation_date = datetime.fromisoformat(fields[3]) if len(fields) >= 4 else None
        completion_date = datetime.fromisoformat(fields[4]) if len(fields) >= 5 else None
    except IndexError as e:
        raise InvalidTaskData("Task must at least have title, description, priority to be created from stdin") from e
    except ValueError as e:
        raise InvalidTaskData("Invalid datetime format")

    return Task.create(
        title=title,
        description=desc,
        priority=priority,
        creation_date=creation_date,
        completion_date=completion_date,
    )