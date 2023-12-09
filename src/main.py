from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.connection import DBConnection, DBManager
from routers import users_router, products_router


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

app.include_router(users_router)
app.include_router(products_router)
