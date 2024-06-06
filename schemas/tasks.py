from pydantic import BaseModel

class TaskModel(BaseModel):
    text: str

class TasksModel(BaseModel):
    tasks: list[str]