from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db  # To be fixed
from app.schemas.task_schema import (
    CreateTaskSchema,
    TaskResponseSchema,
    UpdateTaskSchema,
)
from app.services.task_service import TaskService

router = APIRouter()


@router.get(
    "/tasks", response_model=List[TaskResponseSchema], status_code=status.HTTP_200_OK
)
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    status: Optional[bool] = None,
    search: Optional[str] = None,
):
    service = TaskService(db)  # Keeps business logic organized & testable
    tasks = await service.get_all_tasks(
        limit=limit, offset=offset, status=status, search=search
    )
    return tasks


@router.post(
    "/tasks", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_task(task_in: CreateTaskSchema, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    task = await service.create_task(data=task_in)
    return task


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_in: UpdateTaskSchema,
    task_id: UUID,
    db: AsyncSession = Depends(
        get_db,
    ),
):
    service = TaskService(db)
    task = await service.update_task(task_id, data=task_in)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    await service.delete_task(task_id)
    return {"detail": "Task deleted"}
