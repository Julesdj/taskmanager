from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.user_schema import CreateUserSchema, UserResponseSchema
from app.services.user_service import UserService

router = APIRouter()


@router.post(
    "/users", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
async def register_user(user_in: CreateUserSchema, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.register_user(user_in)
    return user


@router.get("/users/me", response_model=UserResponseSchema)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
