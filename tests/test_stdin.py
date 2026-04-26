from datetime import datetime

import pytest

from src.task_sources.stdin import _parse_and_create
from src.contracts.exceptions.task_exceptions import InvalidTaskData


def test_parse_and_create_valid():
    line = "task1;desc;3;2026-03-23T10:50:00;2026-03-24T12:00:00"
    
    task = _parse_and_create(line)
    
    assert task.title == "task1"
    assert task.description == "desc"
    assert task.priority == 3
    assert isinstance(task.creation_date, datetime)
    assert isinstance(task.completion_date, datetime)


def test_parse_and_create_invalid_priority():
    line = "task1;desc;invalid;2026-03-23T10:50:00"
    
    with pytest.raises(InvalidTaskData):
        _parse_and_create(line)


def test_parse_and_create_short_line():
    line = "task1;desc"
    
    with pytest.raises(
        InvalidTaskData, 
        match="Task must at least have title, description, priority to be created from stdin"
    ):
        _parse_and_create(line)


def test_parse_and_create_invalid_date():
    line = "task1;desc;3;invalid-date;2026-03-24T12:00:00"
    
    with pytest.raises(InvalidTaskData, match="Invalid datetime format"):
        _parse_and_create(line)