from pydantic import BaseModel

class Task(BaseModel):
    text: str