from backend.models import Task
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository:
    @staticmethod
    async def create_task(session: AsyncSession, user_id: int, title: str, description: str = None):
        task = Task(title=title, description=description, user_id=user_id)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def get_user_tasks(session: AsyncSession, user_id: int, is_done: bool = None):
        stmt = select(Task).where(Task.user_id == user_id)
        if is_done is not None:
            stmt = stmt.where(Task.is_done == is_done)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_task(session: AsyncSession, task_id: int, user_id: int, data: dict):
        stmt = (
            update(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def delete_task(session: AsyncSession, task_id: int, user_id: int):
        stmt = delete(Task).where(Task.id == task_id, Task.user_id == user_id)
        await session.execute(stmt)
        await session.commit()
