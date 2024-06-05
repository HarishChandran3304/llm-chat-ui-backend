from fastapi import FastAPI
import json
from models import Task

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/tasks/")
async def add_task(task: Task):
    with open("db.json", "r") as f:
        tasks = json.load(f)
    
    tasks["tasks"].append(task.text)

    with open("db.json", "w") as f:
        json.dump(tasks, f, indent=4)