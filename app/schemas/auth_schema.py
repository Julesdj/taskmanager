from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshSessionSchema(BaseModel):
    id: UUID4
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: datetime
    expires_at: datetime
    revoked_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
