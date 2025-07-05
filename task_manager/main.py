from fastapi import FastAPI

from celery_config.utils import create_celery
from task_manager import task

app = FastAPI()
celery_app = create_celery()

app.include_router(task.router, tags=["Tasks"], prefix="/api/tasks")


@app.get("/api/healthchecker")
def root():
    return {"message": "The API is up."}
