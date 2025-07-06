from datetime import datetime

from sqlmodel import SQLModel

from task_manager.model import TaskStatus


class TaskBaseSchema(SQLModel):
    id: int | None = None
    status: TaskStatus
    validation_error: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class ConfigDict:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class TaskResponse(SQLModel):
    task: TaskBaseSchema


class GetTaskResponse(SQLModel):
    task: TaskBaseSchema
