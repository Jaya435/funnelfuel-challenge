"""
Model for the Task Manager
"""
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
from datetime import datetime, timezone


class TaskStatus(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ERROR = "Error"


class Tasks(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True, description="The ID of the task"
    )
    status: TaskStatus = Field(
        sa_column_kwargs={"default": TaskStatus.NOT_STARTED},
        description="The status of the task",
    )
    validation_error: Optional[str] = Field(
        default=None, description="Validation errors returned from third party APIs"
    )
    created_at: datetime = Field(
        default=datetime.now(timezone.utc),
        nullable=False,
        description="The timestamp of when the task was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        description="The timestamp of when the task was updated",
    )