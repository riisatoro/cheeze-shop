from pydantic import BaseModel


class DefaultResponse(BaseModel):
    message: str
