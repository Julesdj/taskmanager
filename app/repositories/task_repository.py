from typing import Optional, Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task_schema import CreateTaskSchema, UpdateTaskSchema


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

    async def create_task(self, task_in: CreateTaskSchema):
        task = Task(**task_in.model_dump())
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update_task(self, task_id: UUID, task_in: UpdateTaskSchema):
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        for field, value in task_in.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: UUID):
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        await self.db.delete(task)
        await self.db.commit()
