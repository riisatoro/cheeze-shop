from pydantic import BaseModel


class LoginCredentials(BaseModel):
    email: str
    password: str


class Profile(BaseModel):
    username: str
    email: str
