import os
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from schemas import LoginCredentials, JWTResponse


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "random_secret_key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_EXPIRES_AT = int(os.getenv("JWT_ACCESS_EXPIRES_AT", "6000"))
JWT_REFRESH_EXPIRES_AT = int(os.getenv("JWT_REFRESH_EXPIRES_AT", "36000"))

ACCESS_AUDIENCE = "user:access"
REFRESH_AUDIENCE = "user:refresh"


def make_jwt_tokens(creds: LoginCredentials) -> JWTResponse:
    created_at = datetime.now()
    access_expired_at = created_at + timedelta(seconds=JWT_ACCESS_EXPIRES_AT)
    refresh_expired_at = created_at + timedelta(seconds=JWT_REFRESH_EXPIRES_AT)

    access = {
        "email": creds.email,
        "aud": ACCESS_AUDIENCE,
        "iat": created_at.timestamp(),
        "exp": access_expired_at.timestamp(),
    }
    refresh = {
        "email": creds.email,
        "aud": REFRESH_AUDIENCE,
        "iat": created_at.timestamp(),
        "exp": refresh_expired_at.timestamp(),
    }
    return JWTResponse(
        access=jwt.encode(access, SECRET_KEY, algorithm=ALGORITHM),
        refresh=jwt.encode(refresh, SECRET_KEY, algorithm=ALGORITHM),
    )


def verify_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, audience=ACCESS_AUDIENCE, algorithms=[ALGORITHM])
    except (jwt.InvalidAudienceError, jwt.ExpiredSignatureError, jwt.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, audience=REFRESH_AUDIENCE, algorithms=[ALGORITHM])
    except (jwt.InvalidAudienceError, jwt.ExpiredSignatureError, jwt.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token")


def refresh_tokens(refresh_token: str) -> JWTResponse:
    token_payload = verify_refresh_token(refresh_token)
    user_email = token_payload.get("email")
    return make_jwt_tokens(LoginCredentials(email=user_email, password=""))



