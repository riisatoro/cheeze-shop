from fastapi import APIRouter, Depends, UploadFile

from database.connection import DBConnection, DBManager
from database.dependencies import get_user_from_token
from schemas import Product, UserProfile, NewProduct


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/")
async def get_my_profile() -> list[Product]:
    with DBConnection() as conn:
        return DBManager.get_product_list(conn)


@router.post("/new")
async def create_new_product(
    product: NewProduct,
    user: UserProfile = Depends(get_user_from_token)
) -> NewProduct:
    with DBConnection() as conn:
        DBManager.create_product(conn, product)
    return product


@router.patch("/{product_id}")
async def patch_product(
    product_id: int,
    patch_fields: dict,
    user: UserProfile = Depends(get_user_from_token)
) -> Product:
    with DBConnection() as conn:
        DBManager.patch_product(conn, product_id, patch_fields)
        return DBManager.get_product_by_id(conn, product_id)


@router.post("/{product_id}/image")
async def upload_image(
    image: UploadFile,
    product_id: int,
    user: UserProfile = Depends(get_user_from_token)
) -> str:
    image_path = f"media/products/{image.filename}"
    with open(image_path, "wb") as buffer:
        buffer.write(image.file.read())

    with DBConnection() as conn:
        DBManager.patch_product(conn, product_id, {"image": image_path})

    return image_path
