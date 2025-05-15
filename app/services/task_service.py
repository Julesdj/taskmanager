from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_tasks(self):
        result = await self.db.execute(select(Task))
        return result.scalars().all()
