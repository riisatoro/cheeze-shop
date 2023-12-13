from pydantic import BaseModel, field_validator
from security import hash_password


class RegistrationUser(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False


class UserFromDB(BaseModel):
    id: int
    username: str
    email: str
    password: str
    folder_hash: str
    is_admin: bool = False


class UserToDB(BaseModel):
    username: str
    email: str
    password: str
    folder_hash: str
    is_admin: bool = False

    @field_validator("password")
    def make_password(cls, v: str):
        return hash_password(v)


class UserProfile(BaseModel):
    username: str
    email: str
