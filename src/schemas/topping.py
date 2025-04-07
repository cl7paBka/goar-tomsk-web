from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ToppingBase(BaseModel):
    name: str
    price: float

    model_config = ConfigDict(from_attributes=True)

class ToppingCreate(ToppingBase):
    pass

class ToppingRead(ToppingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
