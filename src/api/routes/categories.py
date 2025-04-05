from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get(
    path="/"
)
async def get_categories():
    pass

@router.get(
    path="/{category_id}"
)
async def get_category_by_id(category_id: int):
    pass

@router.post(
    path="/"
)
async def create_category():
    pass

@router.patch(
    path="/{category_id}"
)
async def update_category(category_id: int):
    pass

@router.delete(
    path="/{category_id}"
)
async def delete_category(category_id: int):
    pass