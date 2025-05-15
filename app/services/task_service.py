from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_tasks(self, limit: int = 10, offset: int = 0):
        repository = TaskRepository(self.db)  # Clean separation of data access logic
        result = await repository.get_tasks(limit=limit, offset=offset)
        return result
