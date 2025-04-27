from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import User
from backend.repositories import TaskRepository
from backend.schemas import TaskCreate, TaskUpdate, TaskResponse
from backend.db import get_session
from backend.dependices import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    task = await TaskRepository.create_task(
        session, user_id=user.id_user, title=task_data.title, description=task_data.description
    )
    return task


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    is_done: bool | None = None,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    tasks = await TaskRepository.get_user_tasks(session, user_id=user.id_user, is_done=is_done)
    return tasks


@router.put("/{task_id}/", response_model=None)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    await TaskRepository.update_task(session, task_id, user.id_user, data=task_data.dict(exclude_unset=True))
    return {"message": "Task updated"}


@router.delete("/{task_id}/", response_model=None)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    await TaskRepository.delete_task(session, task_id, user.id_user)
    return {"message": "Task deleted"}
