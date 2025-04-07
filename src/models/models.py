from typing import List, Optional
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    Text,
    Float,
    Boolean,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.db.db import Base
from src.schemas.user import UserRead
from src.schemas.address import UserAddressRead
from src.schemas.category import CategoryRead
from src.schemas.topping import ToppingRead
from src.schemas.product import ProductRead
from src.schemas.product_topping import ProductToppingRead
from src.schemas.order import OrderRead
from src.schemas.order_item import OrderItemRead
from src.schemas.order_item_topping import OrderItemToppingRead
from src.schemas.payment import PaymentRead
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
        return UserRead(
            id=self.id,
            name=self.name,
            phone=self.phone,
            email=self.email,
            role=self.role,
            addresses=[address.to_read_model() for address in self.addresses],
            orders=[order.to_read_model() for order in self.orders],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


# Таблица адресов пользователей
class UserAddress(Base, TimestampMixin):
    __tablename__ = "user_addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    street: Mapped[str] = mapped_column(String(200), nullable=False)
    intercom: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    floor: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    apartment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_private_house: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="addresses")
    orders: Mapped[List["Order"]] = relationship(
        "Order", back_populates="address", cascade="all, delete-orphan"
    )

    def to_read_model(self) -> UserAddressRead:
        return UserAddressRead(
            id=self.id,
            user_id=self.user_id,
            street=self.street,
            intercom=self.intercom,
            floor=self.floor,
            apartment=self.apartment,
            is_private_house=self.is_private_house,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


# Таблица категорий
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    parent: Mapped[Optional["Category"]] = relationship(
        "Category", remote_side=[id], back_populates="subcategories"
    )
    subcategories: Mapped[List["Category"]] = relationship(
        "Category", back_populates="parent", cascade="all, delete-orphan"
    )
    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="subcategory", cascade="all, delete-orphan"
    )

    def to_read_model(self) -> CategoryRead:
        return CategoryRead(
            id=self.id,
            name=self.name,
            parent_id=self.parent_id,
            subcategories=[subcategory.to_read_model() for subcategory in self.subcategories],
            products=[product.to_read_model() for product in self.products],
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

    def to_read_model(self) -> ToppingRead:
        return ToppingRead(
            id=self.id,
            name=self.name,
            price=self.price,
        )


# Таблица продуктов
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    subcategory: Mapped["Category"] = relationship("Category", back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="product", cascade="all, delete-orphan"
    )
    available_toppings: Mapped[List["ProductTopping"]] = relationship(
        "ProductTopping", back_populates="product", cascade="all, delete-orphan"
    )

    def to_read_model(self) -> ProductRead:
        return ProductRead(
            id=self.id,
            name=self.name,
            subcategory_id=self.subcategory_id,
            price=self.price,
            description=self.description,
            subcategory=self.subcategory.to_read_model() if self.subcategory else None,
            order_items=[item.to_read_model() for item in self.order_items],
            available_toppings=[pt.to_read_model() for pt in self.available_toppings],
        )


# Связующая таблица для продуктов и топпингов
class ProductTopping(Base):
    __tablename__ = "product_toppings"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    topping_id: Mapped[int] = mapped_column(ForeignKey("toppings.id", ondelete="CASCADE"), nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="available_toppings")
    topping: Mapped["Topping"] = relationship("Topping", back_populates="product_toppings")

    def to_read_model(self) -> ProductToppingRead:
        return ProductToppingRead(
            id=self.id,
            product_id=self.product_id,
            topping_id=self.topping_id,
            product=self.product.to_read_model() if self.product else None,
            topping=self.topping.to_read_model() if self.topping else None,
        )


# Таблица заказов
class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    address_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user_addresses.id", ondelete="SET NULL"), nullable=True)
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

    def to_read_model(self) -> OrderRead:
        return OrderRead(
            id=self.id,
            user_id=self.user_id,
            address_id=self.address_id,
            delivery_type=self.delivery_type,
            status=self.status,
            total_amount=self.total_amount,
            courier_comment=self.courier_comment,
            delivery_time=self.delivery_time,
            user=self.user.to_read_model() if self.user else None,
            address=self.address.to_read_model() if self.address else None,
            items=[item.to_read_model() for item in self.items],
            payment=self.payment.to_read_model() if self.payment else None,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


# Таблица элементов заказа
class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
    toppings: Mapped[List["OrderItemTopping"]] = relationship(
        "OrderItemTopping", back_populates="order_item", cascade="all, delete-orphan"
    )

    def to_read_model(self) -> OrderItemRead:
        return OrderItemRead(
            id=self.id,
            order_id=self.order_id,
            product_id=self.product_id,
            quantity=self.quantity,
            price=self.price,
            order=self.order.to_read_model() if self.order else None,
            product=self.product.to_read_model() if self.product else None,
            toppings=[topping.to_read_model() for topping in self.toppings],
        )


# Связующая таблица для топпингов в заказе
class OrderItemTopping(Base):
    __tablename__ = "order_item_toppings"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_item_id: Mapped[int] = mapped_column(ForeignKey("order_items.id", ondelete="CASCADE"), nullable=False)
    topping_id: Mapped[int] = mapped_column(ForeignKey("toppings.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order_item: Mapped["OrderItem"] = relationship("OrderItem", back_populates="toppings")
    topping: Mapped["Topping"] = relationship("Topping", back_populates="order_item_toppings")

    def to_read_model(self) -> OrderItemToppingRead:
        return OrderItemToppingRead(
            id=self.id,
            order_item_id=self.order_item_id,
            topping_id=self.topping_id,
            order_item=self.order_item.to_read_model() if self.order_item else None,
            topping=self.topping.to_read_model() if self.topping else None,
        )


# Таблица оплат
class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped["User"] = relationship("User")
    order: Mapped["Order"] = relationship("Order", back_populates="payment")

    def to_read_model(self) -> PaymentRead:
        return PaymentRead(
            id=self.id,
            user_id=self.user_id,
            order_id=self.order_id,
            amount=self.amount,
            status=self.status,
            user=self.user.to_read_model() if self.user else None,
            order=self.order.to_read_model() if self.order else None,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
