from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def register_user(self, user_in: CreateUserSchema):
        hashed_pwd = pwd_context.hash(user_in.hashed_password)
        user_data = user_in.model_copy(update={"hashed_password": hashed_pwd})

        repository = UserRepository(self.db)
        return await repository.create_user(user_data)
