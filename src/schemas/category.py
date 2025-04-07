from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    # Forward ссылки на вложенные категории и продукты
    subcategories: Optional[List["CategoryRead"]] = []
    products: Optional[List["ProductRead"]] = []

    model_config = ConfigDict(from_attributes=True)
