from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserBaseSchema(BaseModel):
    email: str = Field(..., max_length=255)

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(..., max_length=1000)


class UserResponseSchema(UserBaseSchema):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
