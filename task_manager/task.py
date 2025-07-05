import os

from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, status, HTTPException
from sqlmodel import Session

from celery_tasks.tasks import create_campaign_task
from task_manager import schemas, model
from task_manager.db import DB
from task_manager.exceptions import TaskNotFoundError
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
        celery_task = create_campaign_task()
        new_task.id = celery_task.id
        db.create_task(new_task, session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A task with the given details already exists.",
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task.",
        ) from e
    return schemas.TaskResponse(task=schemas.TaskBaseSchema.model_validate(new_task))

@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=schemas.GetTaskResponse)
def get_task(task_id: int):
    db = DB()
    session = Session(db.engine)
    try:
        task = db.read_task(task_id, session)
        return schemas.GetTaskResponse(task=schemas.TaskBaseSchema.model_validate(task))
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the task.",
        ) from e

@router.patch("/{task_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.TaskResponse)
def update_task(task_id: int, payload: schemas.TaskBaseSchema):
    db = DB()
    session = Session(db.engine)
    try:
        task = db.read_task(task_id, session)
        update_data = payload.model_dump(exclude_unset=True)
        db.update_task(
            session,
            task_id,
            task_status=update_data.get('status'),
            validation_error=update_data.get('validation_error')
        )
        return schemas.TaskResponse(task=schemas.TaskBaseSchema.model_validate(task))
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A task with the given details already exists.",
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task.",
        ) from e