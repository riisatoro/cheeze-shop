import os
from typing import List
from fastapi import APIRouter, UploadFile, Depends

from database.dependencies import get_user_from_token
from schemas import UserProfile, DefaultResponse


router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.get("/")
async def get_dir_content(
    directory: str | None = None,
    user: UserProfile = Depends(get_user_from_token),
):
    ...


@router.post("/")
async def upload_files(
    files: List[UploadFile],
    directory: str | None = None,
    user: UserProfile = Depends(get_user_from_token),
) -> DefaultResponse:

    user_dir = os.path.join('media', user.folder_hash, directory or "")
    os.mkdir(user_dir) if not os.path.exists(user_dir) else None

    for file in files:
        file_path = os.path.join(user_dir, file.filename)
        with open(file_path, "wb") as storage_file:
            storage_file.write(await file.read())

    return DefaultResponse(message="Files uploaded successfully")
