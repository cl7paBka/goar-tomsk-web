from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)