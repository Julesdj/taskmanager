from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import tasks as crud
from app.db.deps import get_db  # To be fixed
from app.models.task import Task
from app.schemas.task_schema import (
    CreateTaskSchema,
    TaskResponseSchema,
    UpdateTaskSchema,
)
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponseSchema])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    service = TaskService(db)  # Keeps business logic organized & testable
    tasks = await service.get_all_tasks()
    return tasks


@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task_route(
    task_in: CreateTaskSchema, db: AsyncSession = Depends(get_db)
):
    return await crud.create_task(db, task_in)


@router.patch("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: UUID, task_in: UpdateTaskSchema, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await crud.update_task(db, task, task_in)


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await crud.delete_task(db, task)
    return {"detail": "Task deleted"}
