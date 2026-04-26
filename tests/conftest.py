import uuid
from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from src.contracts.task import Task
from src.contracts.task_source import TaskSource


@pytest.fixture
def mock_tasks():
    id = str(uuid.uuid4())
    return [
        Task(
            id=id, 
            title="Test", 
            description="Desc", 
            priority=1, 
            creation_date=datetime.now(timezone.utc), 
            completion_date=datetime.now(timezone.utc)
        )
    ]


@pytest.fixture
def mock_task_source(mock_tasks):
    source = Mock(spec=TaskSource)
    source.get_tasks.return_value = mock_tasks
    return source