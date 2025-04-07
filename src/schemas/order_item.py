from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    order: Optional["OrderRead"] = None
    product: Optional["ProductRead"] = None
    toppings: Optional[List["OrderItemToppingRead"]] = []

    model_config = ConfigDict(from_attributes=True)
