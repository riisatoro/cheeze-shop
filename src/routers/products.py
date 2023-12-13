from fastapi import APIRouter, Depends, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.connection import DBConnection, DBManager
from database.dependencies import get_user_from_token
from schemas import Product, UserProfile, NewProduct


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_product_list(request: Request):
    with DBConnection() as conn:
        products = DBManager.get_product_list(conn)

    return templates.TemplateResponse("products.html", {"request": request, "products": products})


@router.get("/{product_id}", response_class=HTMLResponse)
async def get_product_by_id(request: Request, product_id: int):
    with DBConnection() as conn:
        product = DBManager.get_product_by_id(conn, product_id)

    return templates.TemplateResponse("product_item.html", {"request": request, "product": product})


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
