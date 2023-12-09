from fastapi import APIRouter, Depends

from database.connection import DBConnection, DBManager
from database.dependencies import get_user_from_token
from schemas import Product, UserProfile


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/")
async def get_my_profile(
        user: UserProfile | None = Depends(get_user_from_token)
) -> list[Product]:
    return []
