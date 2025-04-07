from typing import List, Optional
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    Text,
    Float,
    Boolean,
    CheckConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.db.db import Base
from src.schemas.user import UserRead
from src.utils.enums import UserRole, OrderStatus, DeliveryType

class TimestampMixin:
    """
    Миксин для добавления временных меток создания и обновления.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


# Таблица пользователей
class User(Base, TimestampMixin):
    __tablename__ = "users"
    # TODO проверку на телефон сделать регуляркой для pydantic схемы и для БД, также проработать её под русский номер
    # __table_args__ = (
    #     CheckConstraint(
    #         "phone ~ '^[+]?[\d\\s\\-()]{7,20}$'", name="phone_format_check"
    #     ),
    # )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), nullable=False, default=UserRole.CUSTOMER
    )

    addresses: Mapped[List["UserAddress"]] = relationship(
        "UserAddress", back_populates="user", cascade="all, delete-orphan"
    )
    orders: Mapped[List["Order"]] = relationship(
        "Order", back_populates="user", cascade="all, delete-orphan"
    )

    def to_read_model(self) -> UserRead:
        addresses = [address.to_read_model() for address in self.addresses]
        orders = [order.to_read_model() for order in self.orders]
        return UserRead(
            id=self.id,
            name=self.name,
            phone=self.phone,
            email=self.email,
            role=self.role,
            addresses=addresses,
            orders=orders
        )


# Таблица адресов пользователей
class UserAddress(Base, TimestampMixin):
    __tablename__ = "user_addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    street: Mapped[str] = mapped_column(String(200), nullable=False)
    intercom: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    floor: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    apartment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_private_house: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="addresses")
    orders: Mapped[List["Order"]] = relationship(
        "Order", back_populates="address", cascade="all, delete-orphan"
    )


# Таблица категорий
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )

    parent: Mapped[Optional["Category"]] = relationship(
        "Category", remote_side=[id], back_populates="subcategories"
    )
    subcategories: Mapped[List["Category"]] = relationship(
        "Category", back_populates="parent", cascade="all, delete-orphan"
    )
    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="subcategory", cascade="all, delete-orphan"
    )


# Таблица топпингов
class Topping(Base):
    __tablename__ = "toppings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    product_toppings: Mapped[List["ProductTopping"]] = relationship(
        "ProductTopping", back_populates="topping", cascade="all, delete-orphan"
    )
    order_item_toppings: Mapped[List["OrderItemTopping"]] = relationship(
        "OrderItemTopping", back_populates="topping", cascade="all, delete-orphan"
    )


# Таблица продуктов
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    subcategory: Mapped["Category"] = relationship("Category", back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="product", cascade="all, delete-orphan"
    )
    available_toppings: Mapped[List["ProductTopping"]] = relationship(
        "ProductTopping", back_populates="product", cascade="all, delete-orphan"
    )


# Связующая таблица для продуктов и топпингов
class ProductTopping(Base):
    __tablename__ = "product_toppings"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    topping_id: Mapped[int] = mapped_column(
        ForeignKey("toppings.id", ondelete="CASCADE"), nullable=False
    )

    product: Mapped["Product"] = relationship("Product", back_populates="available_toppings")
    topping: Mapped["Topping"] = relationship("Topping", back_populates="product_toppings")


# Таблица заказов
class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    address_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user_addresses.id", ondelete="SET NULL"), nullable=True
    )
    delivery_type: Mapped[DeliveryType] = mapped_column(
        Enum(DeliveryType, name="delivery_type"), nullable=False, default=DeliveryType.DELIVERY
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"), nullable=False, default=OrderStatus.PENDING
    )
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    courier_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    delivery_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="orders")
    address: Mapped[Optional["UserAddress"]] = relationship("UserAddress", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    payment: Mapped[Optional["Payment"]] = relationship(
        "Payment", back_populates="order", uselist=False, cascade="all, delete-orphan"
    )


# Таблица элементов заказа
class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)


    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
    toppings: Mapped[List["OrderItemTopping"]] = relationship(
        "OrderItemTopping", back_populates="order_item", cascade="all, delete-orphan"
    )


# Связующая таблица для топпингов в заказе
class OrderItemTopping(Base):
    __tablename__ = "order_item_toppings"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_item_id: Mapped[int] = mapped_column(
        ForeignKey("order_items.id", ondelete="CASCADE"), nullable=False
    )
    topping_id: Mapped[int] = mapped_column(
        ForeignKey("toppings.id", ondelete="CASCADE"), nullable=False
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order_item: Mapped["OrderItem"] = relationship("OrderItem", back_populates="toppings")
    topping: Mapped["Topping"] = relationship("Topping", back_populates="order_item_toppings")


# Таблица оплат
class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped["User"] = relationship("User")
    order: Mapped["Order"] = relationship("Order", back_populates="payment")
