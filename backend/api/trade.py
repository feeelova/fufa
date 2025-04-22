from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_session
from backend.schemas import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
    CategoryResponse,
    CategoryBase,
)
from backend.repositories import ExpenseRepository, CategoryRepository
from backend.dependices import get_current_user
from backend.models import User


router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    data: ExpenseCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return await ExpenseRepository.create_expense(session, user.id_user, data)


@router.get("/", response_model=list[ExpenseResponse])
async def get_expenses(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return await ExpenseRepository.get_expenses_by_user(session, user.id_user)


@router.put("/{expense_id}/", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    expense = await ExpenseRepository.update_expense(
        session, expense_id, user.id_user, data
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.delete("/{expense_id}/")
async def delete_expense(
    expense_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    success = await ExpenseRepository.delete_expense(session, expense_id, user.id_user)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted"}


@router.get("/categories/", response_model=list[CategoryResponse])
async def get_categories(session: AsyncSession = Depends(get_session)):
    return await CategoryRepository.get_all_categories(session)


@router.post(
    "/categories/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
async def create_category(
    data: CategoryBase,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can create categories")

    existing = await CategoryRepository.get_category_by_name(session, data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    return await CategoryRepository.create_category(session, data.name)
