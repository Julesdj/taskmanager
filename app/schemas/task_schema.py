from datetime import datetime  # noqa
from typing import Optional

from pydantic import BaseModel


# Shared config base for all schemas
class TaskBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

    class Config:
        orm_mode = True  # Allows SQLAlchemy models to be passed directly


class CreateTaskSchema(TaskBaseSchema):
    pass


class UpdateTaskSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

    class Config:
        orm_model = True


class TaskResponseSchema(TaskBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
