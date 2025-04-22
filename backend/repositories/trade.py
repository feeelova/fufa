from backend.models import Expense, Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ExpenseRepository:
    @staticmethod
    async def create_expense(session: AsyncSession, user_id: int, data):
        expense = Expense(
            user_id=user_id,
            category_id=data.category_id,
            amount=data.amount,
            description=data.description,
        )
        session.add(expense)
        await session.commit()
        await session.refresh(expense)
        return expense

    @staticmethod
    async def get_expenses_by_user(session: AsyncSession, user_id: int):
        result = await session.execute(
            select(Expense)
            .where(Expense.user_id == user_id)
            .order_by(Expense.date.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def update_expense(
        session: AsyncSession, expense_id: int, user_id: int, data
    ):
        result = await session.execute(
            select(Expense).where(Expense.id == expense_id, Expense.user_id == user_id)
        )
        expense = result.scalars().first()
        if not expense:
            return None
        if data.category_id is not None:
            expense.category_id = data.category_id
        if data.amount is not None:
            expense.amount = data.amount
        if data.description is not None:
            expense.description = data.description
        await session.commit()
        await session.refresh(expense)
        return expense

    @staticmethod
    async def delete_expense(session: AsyncSession, expense_id: int, user_id: int):
        result = await session.execute(
            select(Expense).where(Expense.id == expense_id, Expense.user_id == user_id)
        )
        expense = result.scalars().first()
        if not expense:
            return False
        await session.delete(expense)
        await session.commit()
        return True


class CategoryRepository:
    @staticmethod
    async def create_category(session: AsyncSession, name: str):
        new_category = Category(name=name)
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return new_category

    @staticmethod
    async def get_category_by_name(session: AsyncSession, name: str):
        result = await session.execute(select(Category).where(Category.name == name))
        return result.scalars().first()

    @staticmethod
    async def get_all_categories(session: AsyncSession):
        result = await session.execute(select(Category))
        return result.scalars().all()
