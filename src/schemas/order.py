from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from src.utils.enums import DeliveryType, OrderStatus

class OrderBase(BaseModel):
    user_id: int
    address_id: Optional[int] = None
    delivery_type: DeliveryType = DeliveryType.DELIVERY
    status: OrderStatus = OrderStatus.PENDING
    total_amount: float
    courier_comment: Optional[str] = None
    delivery_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    user: Optional["UserRead"] = None
    address: Optional["UserAddressRead"] = None
    items: Optional[List["OrderItemRead"]] = []
    payment: Optional["PaymentRead"] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
