from fastapi import FastAPI

from task_manager.db import DB

# db = DB()

app = FastAPI()


@app.get("/api/healthchecker")
def root():
    return {"message": "The API is up."}
