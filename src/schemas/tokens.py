from pydantic import BaseModel


class JWTResponse(BaseModel):
    access: str
    refresh: str
