from collections.abc import Iterable, Sequence

from src.contracts.task import Task
from src.contracts.task_source import TaskSource


class TaskQueueIterator:
    def __init__(self, task_sources: Sequence[TaskSource]) -> None:
        self.task_sources = task_sources
        self.current_source_index = 0
        self.current_task_iterator = None
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Task:
        while self.current_source_index < len(self.task_sources):
            if self.current_task_iterator is None:
                current_source = self.task_sources[self.current_source_index]
                self.current_task_iterator = iter(current_source.get_tasks())
            try:
                return next(self.current_task_iterator)
            except StopIteration:
                self.current_task_iterator = None
                self.current_source_index += 1
        raise StopIteration

class TaskQueue:
    def __init__(self, task_sources: Sequence[TaskSource]) -> None:
        self.task_sources = []
        for src in task_sources:
            if not isinstance(src, TaskSource):
                raise TypeError("The specified source is not a valid TaskSource")
            self.task_sources.append(src)

    def __iter__(self) -> TaskQueueIterator:
        return TaskQueueIterator(self.task_sources)
    
    def filter_by_completion(self, status: str) -> Iterable[Task]:
        for task in self:
            if task.is_completed == status:
                yield task
    
    def filter_by_priority(self, priority: int) -> Iterable[Task]:
        for task in self:
            if task.priority == priority:
                yield task