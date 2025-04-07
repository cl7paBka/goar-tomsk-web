from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProductToppingBase(BaseModel):
    product_id: int
    topping_id: int

    model_config = ConfigDict(from_attributes=True)

class ProductToppingCreate(ProductToppingBase):
    pass

class ProductToppingRead(ProductToppingBase):
    id: int
    product: Optional["ProductRead"] = None
    topping: Optional["ToppingRead"] = None

    model_config = ConfigDict(from_attributes=True)
