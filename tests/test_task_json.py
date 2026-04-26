import uuid
from pathlib import Path

import pytest

from src.task_sources.task_json import JsonSource


def test_task_json_valid_file(tmp_path: Path):
    # Fixed: Added 'priority', used 'title' instead of 'name', provided a valid UUID
    valid_id = str(uuid.uuid4())
    jsonl_content = f'{{"id": "{valid_id}", "title": "Test", "description": "Desc", "priority": 3, "creation_date": "2026-03-23T10:00:00", "completion_date": "2026-03-24T10:00:00"}}'

    json_file = tmp_path / "tasks.jsonl"
    json_file.write_text(jsonl_content)

    source = JsonSource(json_file)
    tasks = list(source.get_tasks())

    assert len(tasks) == 1
    assert tasks[0].title == "Test"


def test_task_json_empty_file(tmp_path: Path):
    json_file = tmp_path / "empty.jsonl"
    json_file.write_text("")

    source = JsonSource(json_file)
    assert list(source.get_tasks()) == []


def test_task_json_invalid_json(tmp_path: Path):
    # Tests that json.JSONDecodeError is caught and skipped
    json_file = tmp_path / "invalid.jsonl"
    json_file.write_text('{"id": "1" invalid json')

    source = JsonSource(json_file)
    tasks = list(source.get_tasks())
    assert len(tasks) == 0


def test_task_json_invalid_task_data(tmp_path: Path):
    # Tests that valid JSON with missing/invalid fields (TaskError) is caught and skipped
    # E.g., missing 'priority' and providing an invalid UUID string
    jsonl_content = '{"id": "not-a-uuid", "title": "Test", "creation_date": "2026-03-23T10:00:00"}'
    
    json_file = tmp_path / "invalid_task.jsonl"
    json_file.write_text(jsonl_content)

    source = JsonSource(json_file)
    tasks = list(source.get_tasks())
    
    # Task should be skipped, returning 0 tasks
    assert len(tasks) == 0