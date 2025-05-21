from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserSchema


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def register_user(self, user_in: CreateUserSchema):
        repository = UserRepository(self.db)
        existing_user = await repository.get_by_email(user_in.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

        hashed_pwd = hash_password(user_in.hashed_password)
        user_data = user_in.model_copy(update={"hashed_password": hashed_pwd})

        return await repository.create_user(user_data)
