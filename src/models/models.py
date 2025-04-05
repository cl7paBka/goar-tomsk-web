from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, Float, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.db.db import Base
from src.utils.enums import UserRole, OrderStatus, MeatType, DeliveryType


# Таблица пользователей
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # TODO сделать регулярку на проверку корректности номера телефона + по длине тоже переработать
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())

    addresses = relationship("UserAddress", back_populates="user")
    orders = relationship("Order", back_populates="user")


# Таблица адресов пользователей
class UserAddress(Base):
    __tablename__ = "user_addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    street: Mapped[str] = mapped_column(String(200), nullable=False)
    intercom: Mapped[str] = mapped_column(String(20), nullable=True)
    floor: Mapped[int] = mapped_column(Integer, nullable=True)
    apartment: Mapped[str] = mapped_column(String(20), nullable=True)
    is_private_house: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")


# Таблица категорий
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)

    subcategories = relationship("Category", back_populates="parent")
    parent = relationship("Category", back_populates="subcategories", remote_side=[id])
    products = relationship("Product", back_populates="subcategory")


# Таблица топпингов
class Topping(Base):
    __tablename__ = "toppings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    product_toppings = relationship("ProductTopping", back_populates="topping")


# Таблица продуктов
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    has_meat_options: Mapped[bool] = mapped_column(Boolean, default=False)  # Указывает, можно ли выбирать мясо

    subcategory = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    available_toppings = relationship("ProductTopping", back_populates="product")


# Связующая таблица для продуктов и топпингов
class ProductTopping(Base):
    __tablename__ = "product_toppings"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    topping_id: Mapped[int] = mapped_column(ForeignKey("toppings.id"), nullable=False)

    product = relationship("Product", back_populates="available_toppings")
    topping = relationship("Topping", back_populates="product_toppings")


# Таблица заказов
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("user_addresses.id"), nullable=True)  # Изменено на nullable для самовывоза
    delivery_type: Mapped[DeliveryType] = mapped_column(Enum(DeliveryType), nullable=False, default=DeliveryType.DELIVERY)  # Добавлено поле доставки/самовывоза
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    courier_comment: Mapped[str] = mapped_column(Text, nullable=True)
    delivery_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)  # Добавлено время доставки, null = "как можно быстрее"
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())

    user = relationship("User", back_populates="orders")
    address = relationship("UserAddress", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)


# Таблица элементов заказа
class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    meat_type: Mapped[MeatType] = mapped_column(Enum(MeatType),
                                                nullable=True)  # Опционально, только если has_meat_options=True

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    toppings = relationship("OrderItemTopping", back_populates="order_item")


# Связующая таблица для топпингов в заказе
class OrderItemTopping(Base):
    __tablename__ = "order_item_toppings"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_item_id: Mapped[int] = mapped_column(ForeignKey("order_items.id"), nullable=False)
    topping_id: Mapped[int] = mapped_column(ForeignKey("toppings.id"), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order_item = relationship("OrderItem", back_populates="toppings")
    topping = relationship("Topping")


# Таблица оплат
class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, unique=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())

    user = relationship("User")
    order = relationship("Order", back_populates="payment")