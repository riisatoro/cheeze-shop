from pydantic import BaseModel


class LoginCredentials(BaseModel):
    email: str
    password: str


class UserProfile(BaseModel):
    username: str
    email: str
    folder_hash: str
