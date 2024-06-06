from fastapi import APIRouter
import json
from ..schemas.tasks import TaskModel, TasksModel

router = APIRouter()


@router.get("/tasks/")
async def get_tasks() -> TasksModel:
    with open("db.json", "r") as f:
        tasks = json.load(f)["tasks"]
    return {"tasks": tasks}

@router.post("/tasks/")
async def add_task(task: TaskModel) -> TaskModel:
    with open("db.json", "r") as f:
        db = json.load(f)
        tasks = db["tasks"]
    
    tasks.append(task.text)

    db["tasks"] = tasks
    with open("db.json", "w") as f:
        json.dump(db, f, indent=4)
    
    return task