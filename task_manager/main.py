from fastapi import FastAPI

from task_manager import task

app = FastAPI()

app.include_router(task.router, tags=["Tasks"], prefix="/api/tasks")


@app.get("/api/healthchecker")
def root():
    return {"message": "The API is up."}
