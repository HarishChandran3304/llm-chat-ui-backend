from fastapi import APIRouter
import json
from ..schemas.tasks import GetTasksModel, AddTaskModel

router = APIRouter()


@router.get("/tasks/")
async def get_tasks() -> GetTasksModel:
    with open("db.json", "r") as f:
        tasks = json.load(f)
    return tasks

@router.post("/tasks/")
async def add_task(task: AddTaskModel) -> AddTaskModel:
    with open("db.json", "r") as f:
        tasks = json.load(f)
    
    tasks["tasks"].append(task.text)

    with open("db.json", "w") as f:
        json.dump(tasks, f, indent=4)
    
    return task