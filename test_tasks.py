import pytest, json 
import tasks
from datetime import datetime

from tasks import (
    load_tasks,
    add_task,
    delete_task,
    update_task,
    update_status,
    list_tasks,
)


@pytest.fixture(autouse=True)


def setup(monkeypatch, tmp_path):
    test_file = tmp_path / "tests_tasks.json"
    test_file.touch()
    monkeypatch.setattr(tasks, "TASKS_FILE", str(test_file))
    with open(test_file, "w") as f:
        f.write("[]")
    yield
@pytest.fixture 


def sample_tasks():
    # testing data
    tasks = [
        {
            "id": 1,
            "description": "Task 1",
            "status": "todo",
            "createdAt": datetime.now().ctime(),
            "updatedAt": datetime.now().ctime(),
        },
        {
            "id": 2,
            "description": "Task 2",
            "status": "todo",
            "createdAt": datetime.now().ctime(),
            "updatedAt": datetime.now().ctime(),
        },
    ]
    return tasks

def test_add_task(tmp_path, monkeypatch):
    test_file = tmp_path / "test_tasks.json"
    monkeypatch.setattr("tasks.TASKS_FILE", str(test_file))

    add_task("Test Task")
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Test Task"



def test_update_task(sample_tasks, monkeypatch):
    from tasks import save_tasks
    save_tasks(sample_tasks)

    update_task("1", "Updated description")
    tasks = load_tasks()
    

    updated_task = next(task for task in tasks if task["id"] == 1)
    assert updated_task["description"] == "Updated description"

def test_update_status(sample_tasks, monkeypatch):
    from tasks import save_tasks
    save_tasks(sample_tasks)

    monkeypatch.setattr("builtins.input", lambda *_: "3")
    update_status("1") 
    
    tasks = load_tasks()
    updated_task = next(task for task in tasks if task["id"] == 1)
    assert updated_task["status"] == "done"  

def test_filter_tasks(sample_tasks, monkeypatch, capsys):
    from tasks import save_tasks, filter_tasks
    save_tasks(sample_tasks)

    monkeypatch.setattr("builtins.input", lambda *args: "2")  
    filter_tasks()

    captured = capsys.readouterr()
    assert "Done" in captured.out

