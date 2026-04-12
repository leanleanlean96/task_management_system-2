from collections.abc import Iterable, Sequence

from src.contracts.task import Task
from src.contracts.task_source import TaskSource


class TaskManagementSystem:
    """Task Management system class for managing tasks"""

    def __init__(self, task_sources: Sequence[TaskSource]) -> None:
        self.task_sources = task_sources or []

    def iter_tasks(self) -> Iterable[Task]:
        for src in self.task_sources:
            if not isinstance(src, TaskSource):
                raise TypeError("The specified source is not a valid TaskSource")
            for task in src.get_tasks():
                yield task
