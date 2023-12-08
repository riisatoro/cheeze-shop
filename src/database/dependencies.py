from typing import Annotated

from fastapi import Header

from database.connection import DBConnection, DBManager
from security.tokens import verify_access_token
from schemas import UserProfile


def get_user_from_token(X_ACCESS_TOKEN: Annotated[str, Header()]) -> UserProfile:
    token_payload = verify_access_token(X_ACCESS_TOKEN)
    user_email = token_payload.get("email")

    with DBConnection() as cursor:
        db_user = DBManager.get_user_by_email(cursor, user_email)

    return UserProfile(**db_user.model_dump())
