from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import tasks
from .routers import conversations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(tasks.router)
app.include_router(conversations.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}