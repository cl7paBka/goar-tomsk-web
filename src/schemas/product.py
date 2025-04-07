from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    name: str
    subcategory_id: int
    price: float
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    # Forward ссылки на связанные схемы
    subcategory: Optional["CategoryRead"] = None
    order_items: Optional[List["OrderItemRead"]] = []
    available_toppings: Optional[List["ProductToppingRead"]] = []

    model_config = ConfigDict(from_attributes=True)
