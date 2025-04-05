from typing import Annotated, List

from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    path="/register"
)
async def register_user(

):
    pass


@router.post(
    path="/login"
)
async def login_user(

):
    pass


@router.get(
    path="/me"
)
async def whoami(

):
    pass


@router.patch(
    path="/me"
)
async def update_user(

):
    pass


@router.delete(
    path="/me"
)
async def delete_user(

):
    pass
