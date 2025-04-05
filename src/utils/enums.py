from enum import Enum


# Перечисления для ролей и статусов
class UserRole(Enum):
    CUSTOMER = "customer"
    ADMINISTRATOR = "administrator"


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    PREPARING = "preparing"
    DELIVERING = "delivering"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MeatType(Enum):
    CHICKEN = "chicken"
    PORK = "pork"
    BEEF = "beef"


class DeliveryType(Enum):
    DELIVERY = "delivery"
    PICKUP = "pickup"
