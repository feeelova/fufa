from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    category_id: int
    amount: float
    description: Optional[str] = None


class ExpenseUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: int
    category: CategoryResponse
    amount: float
    description: Optional[str]
    date: datetime

    class Config:
        from_attributes = True
