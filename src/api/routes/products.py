from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get(
    path="/"
)
async def get_products():
    pass

@router.get(
    path="/{product_id}"
)
async def get_product_by_id(product_id: int):
    pass

@router.post(
    path="/"
)
async def create_product():
    pass

@router.patch(
    path="/{product_id}"
)
async def update_product(product_id: int):
    pass

@router.delete(
    path="/{product_id}"
)
async def delete_product(product_id: int):
    pass