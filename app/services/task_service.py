from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_tasks(self):
        repository = TaskRepository(self.db)  # Clean separation of data access logic
        result = await repository.get_all_tasks()
        return result
