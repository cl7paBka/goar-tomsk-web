from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, constr
from datetime import datetime

from src.utils.enums import UserRole

# Регулярное выражение для проверки русского номера телефона
# RUSSIAN_PHONE_REGEX = r'^(?:\+7|8)\s?\(?\d{3}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}$'

class UserBase(BaseModel):
    name: str
    # phone: constr(regex=RUSSIAN_PHONE_REGEX)
    phone: str
    email: EmailStr
    role: UserRole = UserRole.CUSTOMER

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    # Forward-ссылки оформлены как строки – они будут разрешены после вызова model_rebuild()
    addresses: Optional[List["UserAddressRead"]] = []
    orders: Optional[List["OrderRead"]] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
