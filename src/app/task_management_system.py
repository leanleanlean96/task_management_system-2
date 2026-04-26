from collections.abc import Iterable, Sequence

from src.app.task_queue import TaskQueue
from src.contracts.task import Task
from src.contracts.task_source import TaskSource


class TaskManagementSystem:
    """Task Management system class for managing tasks"""

    def __init__(self, task_sources: Sequence[TaskSource]) -> None:
        self.task_queue = TaskQueue(task_sources)

    def iter_tasks(self) -> Iterable[Task]:
            yield from self.task_queue
    
    def iter_completed_tasks(self) -> Iterable[Task]:
        yield from self.task_queue.filter_by_completion("Completed")

    def iter_tasks_by_priority(self, priority: int) -> Iterable[Task]:
        yield from self.task_queue.filter_by_priority(priority)
