from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user_schema import CreateUserSchema


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, user_in: CreateUserSchema):
        user = User(**user_in.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))

        return result.scalars().first()
