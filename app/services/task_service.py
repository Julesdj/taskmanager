from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import CreateTaskSchema


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_tasks(
        self,
        limit: int = 10,
        offset: int = 0,
        status: Optional[bool] = None,
        search: Optional[str] = None,
    ):
        repository = TaskRepository(self.db)  # Clean separation of data access logic
        result = await repository.get_tasks(
            limit=limit, offset=offset, status=status, search=search
        )
        return result

    async def create_task(self, data: CreateTaskSchema):
        return await TaskRepository(self.db).create_task(data)
