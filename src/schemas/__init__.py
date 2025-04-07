from .common import TimestampSchema
from .user import UserBase, UserCreate, UserRead
from .address import UserAddressBase, UserAddressCreate, UserAddressRead
from .category import CategoryBase, CategoryCreate, CategoryRead
from .topping import ToppingBase, ToppingCreate, ToppingRead
from .product import ProductBase, ProductCreate, ProductRead
from .product_topping import ProductToppingBase, ProductToppingCreate, ProductToppingRead
from .order import OrderBase, OrderCreate, OrderRead
from .order_item import OrderItemBase, OrderItemCreate, OrderItemRead
from .order_item_topping import OrderItemToppingBase, OrderItemToppingCreate, OrderItemToppingRead
from .payment import PaymentBase, PaymentCreate, PaymentRead

# Обновляем forward-ссылки после импорта всех схем
UserRead.model_rebuild()
UserAddressRead.model_rebuild()
CategoryRead.model_rebuild()
ToppingRead.model_rebuild()
ProductRead.model_rebuild()
ProductToppingRead.model_rebuild()
OrderRead.model_rebuild()
OrderItemRead.model_rebuild()
OrderItemToppingRead.model_rebuild()
PaymentRead.model_rebuild()
