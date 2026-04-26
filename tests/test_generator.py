from datetime import datetime, timedelta

import pytest

from src.contracts.task import Task
from src.task_sources.generator_data.data_lists import name_list
from src.task_sources.task_generator import TaskGenerator


@pytest.fixture
def sample_data():
    base_date = datetime.now()
    

    cr_dates = [base_date, base_date + timedelta(hours=1)]
    

    comp_dates = [base_date + timedelta(days=1), base_date + timedelta(days=2), None]
    
    return {
        "names": name_list[:3],
        "descs": ["desc1", "desc2", "desc3"],
        "dates": cr_dates,
        "comp_dates": comp_dates,
    }


@pytest.fixture
def generator(sample_data):
    return TaskGenerator(
        sample_data["names"],
        sample_data["descs"],
        sample_data["dates"],
        sample_data["comp_dates"],
    )


def test_task_generator_init(generator, sample_data):
    assert generator.name_list == sample_data["names"]
    assert len(generator.name_list) == 3


def test_get_tasks_yields_tasks(generator):
    tasks = list(generator.get_tasks())
    assert 1 <= len(tasks) <= 33
    assert all(isinstance(task, Task) for task in tasks)


def test_get_tasks_random_properties(generator, sample_data):
    tasks = list(generator.get_tasks())
    task = tasks[0]

    assert task.id != ""
    assert task.title in sample_data["names"]
    assert task.description in sample_data["descs"]
    assert task.creation_date in sample_data["dates"]


def test_get_tasks_completion_date_logic(generator):
    tasks = list(generator.get_tasks())
    
    completed_task = next((t for t in tasks if t.is_completed == "Completed"), None)

    if completed_task:
        assert completed_task.completion_date is not None