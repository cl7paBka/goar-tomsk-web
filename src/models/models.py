from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.db.db import Base
from src.utils.enums import Role, OrderStatus, TransmissionType, EngineType
from src.schemas.users import UserSchema
from src.schemas.cars import CarSchema
from src.schemas.orders import OrderSchema


class Users(Base):
    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    def to_read_model(self):
        pass


class Products(Base):
    __tablename__ = "products"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    def to_read_model(self):
        pass


class Orders(Base):
    __tablename__ = "orders"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    def to_read_model(self):
        pass
