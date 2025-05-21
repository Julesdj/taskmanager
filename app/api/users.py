from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
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
