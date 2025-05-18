from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import CreateTaskSchema, UpdateTaskSchema


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

    async def update_task(self, task_id: UUID, data: UpdateTaskSchema):
        repository = TaskRepository(self.db)
        return await repository.update_task(task_id, data)

    async def delete_task(self, task_id: UUID):
        repository = TaskRepository(self.db)
        await repository.delete_task(task_id)
