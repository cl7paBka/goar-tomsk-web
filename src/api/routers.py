from src.api.routes.users import router as users_router
from src.api.routes.products import router as products_router
from src.api.routes.categories import router as categories_router
from src.api.routes.orders import router as orders_router

all_routers = [
    users_router,
    products_router,
    categories_router,
    orders_router
]
