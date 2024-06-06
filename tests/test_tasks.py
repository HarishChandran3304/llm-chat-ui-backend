from fastapi.testclient import TestClient
from ..main import app
import pytest
import json
from ..schemas.tasks import TaskModel

@pytest.fixture
def client():
    return TestClient(app)

def test_get_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json()["tasks"], list)

    with open("db.json") as f:
        tasks = json.load(f)["tasks"]
    assert response.json()["tasks"] == tasks

def test_add_task(client):
    new_task = TaskModel(text="Test task")
    
    response = client.post("/tasks/", json=new_task.model_dump())
    assert response.status_code == 200
    assert response.json() == new_task.model_dump()

    with open("db.json") as f:
        db = json.load(f)
        tasks = db["tasks"]
        tasks.remove(new_task.text)
    
    with open("db.json", "w") as f:
        json.dump(db, f, indent=4)
