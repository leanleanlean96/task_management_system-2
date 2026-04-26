import inspect
import pytest
from datetime import datetime, timezone
from src.contracts.task import Task
from src.app.task_queue import TaskQueue

@pytest.fixture
def sample_tasks():
    t1 = Task.create(title="Task 1", priority=1)
    t2 = Task.create(title="Task 2", priority=3)
    t3 = Task.create(title="Task 3", priority=5)
    t3.complete(datetime.now(timezone.utc))
    
    class DummySource:
        def __init__(self, tasks):
            self.tasks = tasks
            self.name = "Dummy"
        def get_tasks(self):
            yield from self.tasks

    return [DummySource([t1, t2]), DummySource([t3])]

def test_queue_repeated_traversal(sample_tasks):

    queue = TaskQueue(sample_tasks)
    
    pass_1 = [t.title for t in queue]
    pass_2 = [t.title for t in queue]
    
    assert pass_1 == pass_2 == ["Task 1", "Task 2", "Task 3"]

def test_manual_stop_iteration(sample_tasks):
    queue = TaskQueue(sample_tasks)
    iterator = iter(queue)
    
    next(iterator) # Task 1
    next(iterator) # Task 2
    next(iterator) # Task 3
    

    with pytest.raises(StopIteration):
        next(iterator)

def test_lazy_filters_are_generators(sample_tasks):

    queue = TaskQueue(sample_tasks)
    
    status_filter = queue.filter_by_completion("Completed")
    priority_filter = queue.filter_by_priority(3)
    
    assert inspect.isgenerator(status_filter)
    assert inspect.isgenerator(priority_filter)
    
    assert len(list(status_filter)) == 1
    assert len(list(priority_filter)) == 2