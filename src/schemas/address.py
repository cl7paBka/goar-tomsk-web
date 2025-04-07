from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserAddressBase(BaseModel):
    user_id: int
    street: str
    intercom: Optional[str] = None
    floor: Optional[int] = None
    apartment: Optional[str] = None
    is_private_house: bool = False

    model_config = ConfigDict(from_attributes=True)

class UserAddressCreate(UserAddressBase):
    pass

class UserAddressRead(UserAddressBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
