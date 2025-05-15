from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task_schema import CreateTaskSchema, UpdateTaskSchema


async def get_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()


async def create_task(db: AsyncSession, task_in: CreateTaskSchema):
    task = Task(**task_in.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update_task(db: AsyncSession, task: Task, task_in: UpdateTaskSchema):
    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task: Task):
    await db.delete(task)
    await db.commit()
