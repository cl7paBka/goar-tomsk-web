from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PaymentBase(BaseModel):
    user_id: int
    order_id: int
    amount: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int
    user: Optional["UserRead"] = None
    order: Optional["OrderRead"] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
