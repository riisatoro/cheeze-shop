from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.connection import DBConnection, DBManager


@asynccontextmanager
async def prepare_db(_: FastAPI):
    print()
    with DBConnection() as cursor:
        DBManager.create_database(cursor)
    yield


app = FastAPI(
    title="Files synchronize",
    description="Synchronize files between multiple machines",
    lifespan=prepare_db,
)
