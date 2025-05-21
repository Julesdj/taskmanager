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
