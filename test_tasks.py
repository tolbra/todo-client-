import pytest
import os
from tasks import TASKS_FILE  # if needed for reference
import tasks  # Import the tasks module

@pytest.fixture(autouse=True)
def temp_tasks_file(tmp_path, monkeypatch):
    # Create a temporary file   
    test_file = tmp_path / "tests.json"
    # Initialize the file with an empty JSON array
    test_file.write_text("[]")
    # Override the TASKS_FILE in the tasks module with our temporary file's path
    monkeypatch.setattr(tasks, "TASKS_FILE", str(test_file))
    yield
    # Cleanup: Remove the temporary file if it exists
    if test_file.exists():
        test_file.unlink()


def test_which_tasks():
    print("DEBUG: tasks module is located at:", tasks.__file__)
    print("DEBUG: Current working directory:", os.getcwd())
    assert False  # Force test to fail so we can see the output

def test_add_task_single():
    # Initially, load_tasks() should return an empty list.
    tasks_list = tasks.load_tasks()
    assert tasks_list == []  # Confirm it's empty.

    # Add a single task.
    tasks.add_task("hello, world")
    
    # Reload the tasks from the file.
    tasks_list = tasks.load_tasks()
    assert len(tasks_list) == 1
    task = tasks_list[0]
    assert task['description'] == "hello, world"
    assert task['status'] == "todo"
    # Since add_task sets task_id to 1 if no tasks exist.
    assert task['id'] == 1
