import pytest

from src.app.task_management_system import TaskManagementSystem
from src.contracts.task_source import TaskSource


def test_init_empty_sources():
    system = TaskManagementSystem([])
    assert system.task_queue.task_sources == []


def test_init_with_sources(mock_task_source: TaskSource):
    system = TaskManagementSystem([mock_task_source])
    assert len(system.task_queue.task_sources) == 1


def test_iter_tasks_empty():
    system = TaskManagementSystem([])
    assert list(system.iter_tasks()) == []


def test_iter_tasks_valid_source(mock_task_source: TaskSource, mock_tasks):
    system = TaskManagementSystem([mock_task_source])
    tasks = list(system.iter_tasks())
    assert len(tasks) == 1
    assert tasks[0] == mock_tasks[0]


def test_iter_tasks_invalid_source():
    with pytest.raises(TypeError, match="not a valid TaskSource"):
        TaskManagementSystem(["not a TaskSource"])