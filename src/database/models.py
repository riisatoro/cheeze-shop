from pydantic import BaseModel, field_validator
from security import hash_password


class RegistrationUser(BaseModel):
    username: str
    email: str
    password: str


class UserFromDB(BaseModel):
    id: int
    username: str
    email: str
    password: str
    folder_hash: str


class UserToDB(BaseModel):
    username: str
    email: str
    password: str
    folder_hash: str

    @field_validator("password")
    def make_password(cls, v: str):
        return hash_password(v)


class UserProfile(BaseModel):
    username: str
    email: str
