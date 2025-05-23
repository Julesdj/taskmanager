from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserSchema


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repository = UserRepository(self.db)

    async def register_user(self, user_in: CreateUserSchema):
        existing_user = await self.repository.get_by_email(user_in.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

        hashed_pwd = hash_password(user_in.password)
        user_dict = user_in.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hashed_pwd

        return await self.repository.create_user(user_dict)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.repository.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
            )

        return user
