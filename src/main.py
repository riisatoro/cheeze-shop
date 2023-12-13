import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from database.connection import DBConnection, DBManager
from routers import users_router, products_router, orders_router


@asynccontextmanager
async def prepare_db(_: FastAPI):
    with DBConnection() as cursor:
        DBManager.create_database(cursor)
    yield


app = FastAPI(
    title="Local farm cheeze shop",
    description="API for selling cheeze from local farms",
    lifespan=prepare_db,
)

app.mount("/media", StaticFiles(directory="media"), name="static")


@app.get("/")
async def root(request: Request):
    request_id = request.cookies.get("request_id", uuid.uuid4().hex)
    response = RedirectResponse("/products")
    response.set_cookie(key="request_id", value=request_id)
    return response


app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)
