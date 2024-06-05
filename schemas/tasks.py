from pydantic import BaseModel

class AddTaskModel(BaseModel):
    text: str

class GetTasksModel(BaseModel):
    tasks: list[str]