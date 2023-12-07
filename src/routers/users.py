from fastapi import APIRouter

from database.connection import DBConnection, DBManager
from database.models import User
from schemas import DefaultResponse, Profile, LoginCredentials


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/new")
async def create_user(user: User) -> DefaultResponse:
    with DBConnection() as cursor:
        DBManager.create_user(cursor, user)
        return DefaultResponse(message="User created successfully")


@router.post("/login")
async def login_user(credentials: LoginCredentials) -> Profile:
    ...
