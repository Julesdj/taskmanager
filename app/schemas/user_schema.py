from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field


class UserBaseSchema(BaseModel):
    email: EmailStr = Field(..., max_length=255)

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(UserBaseSchema):
    password: str = Field(..., max_length=1000)


class UserResponseSchema(UserBaseSchema):
    id: UUID4
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
