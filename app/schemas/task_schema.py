from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# Shared base for all schemas
class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class CreateTaskSchema(TaskBaseSchema):
    pass


class UpdateTaskSchema(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class TaskResponseSchema(TaskBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
