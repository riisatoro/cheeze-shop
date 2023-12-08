from fastapi import APIRouter, HTTPException, Depends
from sqlite3 import IntegrityError

from database.connection import DBConnection, DBManager
from database.models import RegistrationUser
from database.dependencies import get_user_from_token
from schemas import DefaultResponse, UserProfile, LoginCredentials, JWTResponse
from security import check_password, make_jwt_tokens


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/new")
async def create_user(user: RegistrationUser) -> DefaultResponse:
    try:
        with DBConnection() as cursor:
            DBManager.create_user(cursor, user)
            return DefaultResponse(message="User created successfully")
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Unable to create user.")


@router.post("/login")
async def login_user(credentials: LoginCredentials) -> JWTResponse:
    with DBConnection() as cursor:
        user = DBManager.get_user_by_email(cursor, credentials.email)

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    if not check_password(credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials.")

    return make_jwt_tokens(credentials)


@router.get("/me")
async def get_my_profile(
        user: UserProfile = Depends(get_user_from_token)
) -> UserProfile:
    return user
