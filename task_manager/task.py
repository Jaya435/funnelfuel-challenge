import os

from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, status, HTTPException
from sqlmodel import Session

from task_manager import schemas, model
from task_manager.db import DB
from task_manager.logger import create_logger

# Extract the filename without extension
filename = os.path.splitext(os.path.basename(__file__))[0]

logger = create_logger(logger_name=filename)
router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
def create_task(payload: schemas.TaskBaseSchema):
    db = DB()
    session = Session(db.engine)
    try:
        new_task = model.Tasks(**payload.model_dump())
        db.create_task(new_task, session)
    except IntegrityError as e:
        # Log the error or handle it as needed
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with the given details already exists.",
        ) from e
    except Exception as e:
        # Handle other types of database errors
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task.",
        ) from e

    # Convert the SQLAlchemy model instance to a Pydantic model
    task_schema = schemas.TaskBaseSchema.model_validate(new_task)
    # Return the successful creation response
    return schemas.TaskResponse(Task=task_schema)
