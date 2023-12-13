import uuid
from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database.connection import DBConnection, DBManager
from schemas import OrderDetails


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


templates = Jinja2Templates(directory="templates")


@router.post("/add", response_class=HTMLResponse)
def add_order(request: Request, product_id: Annotated[int, Form()], quantity: Annotated[int, Form()]):
    order_details = OrderDetails(product_id=product_id, quantity=quantity)
    request_id = request.cookies.get("request_id")

    with DBConnection() as conn:
        order = DBManager.get_order(conn, request_id)
        if not order:
            order = DBManager.create_order(conn, request_id)

        DBManager.create_order_item(conn, order.id, order_details)

    return RedirectResponse(url="/products", status_code=303)


@router.get("/", response_class=HTMLResponse)
def get_orders(request: Request):
    request_id = request.cookies.get("request_id")

    order_items = []
    with DBConnection() as conn:
        order = DBManager.get_order(conn, request_id)
        if order:
            order_items = DBManager.get_order_items(conn, order.id)

    return templates.TemplateResponse(
        "get_orders.html", {"request": request, "order": order, "order_items": order_items}
    )
