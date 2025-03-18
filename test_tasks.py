import pytest, json 
import tasks

from tasks import (
    load_tasks,
    add_task
)

TASKS_FILE: str = "tests.json"


@pytest.fixture(autouse=True)


def override_tasks_file(monkeypatch, tmp_path):
    test_file = tmp_path / "tests.json"
    test_file.touch()
    monkeypatch.setattr(tasks, "TASKS_FILE", str(test_file))
    yield

def test_add_task() -> None:
    tasks_list = load_tasks()
    assert tasks_list == [], "The JSON file should be empty"
    add_task("Let's test")
    tasks_list = load_tasks()
    assert len(tasks_list) == 1