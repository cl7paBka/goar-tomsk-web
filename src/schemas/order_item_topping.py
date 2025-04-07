from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

class OrderItemToppingBase(BaseModel):
    order_item_id: int
    topping_id: int
    price: float

    model_config = ConfigDict(from_attributes=True)

class OrderItemToppingCreate(OrderItemToppingBase):
    pass

class OrderItemToppingRead(OrderItemToppingBase):
    id: int
    order_item: Optional["OrderItemRead"] = None
    topping: Optional["ToppingRead"] = None

    model_config = ConfigDict(from_attributes=True)
