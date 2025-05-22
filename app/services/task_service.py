from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import CreateTaskSchema, UpdateTaskSchema


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = TaskRepository(self.db)

    async def get_all_tasks(
        self,
        limit: int = 10,
        offset: int = 0,
        status: Optional[bool] = None,
        search: Optional[str] = None,
        order_by: str = "created_at",
        order: str = "desc",
    ):
        result = await self.repository.get_tasks(
            limit=limit,
            offset=offset,
            status=status,
            search=search,
            order_by=order_by,
            order=order,
        )
        return result

    async def create_task(self, data: CreateTaskSchema):
        return await self.repository.create_task(data)

    async def update_task(self, task_id: UUID, data: UpdateTaskSchema):
        return await self.repository.update_task(task_id, data)

    async def delete_task(self, task_id: UUID):
        await self.repository.delete_task(task_id)
