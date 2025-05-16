from typing import Optional, Sequence

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tasks(
        self,
        limit: int = 10,
        offset: int = 0,
        status: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> Sequence[Task]:
        """Fetch all tasks from the database with pagination."""
        stmt = select(Task)
        filters = []

        if status is not None:  # status should be boolean: True or False
            filters.append(Task.is_completed == status)

        if search:
            filters.append(
                or_(
                    Task.title.ilike(f"%{search}%"),
                    Task.description.ilike(f"%{search}%"),
                )
            )

        if filters:
            stmt = stmt.where(*filters)

        stmt = stmt.limit(limit).offset(offset)

        result = await self.db.execute(stmt)
        return result.scalars().all()
