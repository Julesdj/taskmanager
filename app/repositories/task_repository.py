from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tasks(self, limit: int = 10, offset: int = 0) -> List[Task]:
        """Fetch all tasks from the database with pagination."""
        pagination = select(Task).limit(limit).offset(offset)
        result = await self.db.execute(pagination)
        return result.scalars().all()
