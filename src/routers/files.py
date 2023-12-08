import os
from typing import List
from fastapi import APIRouter, UploadFile, Depends, HTTPException

from database.dependencies import get_user_from_token
from schemas import UserProfile, DefaultResponse, FolderContent, FileInfo


router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.get("/")
async def get_dir_content(
    directory: str | None = None,
    user: UserProfile = Depends(get_user_from_token),
) -> FolderContent:
    user_dir = os.path.join('media', user.folder_hash, directory or "")
    if not os.path.exists(user_dir):
        if directory:
            raise HTTPException(status_code=404, detail='Folder not found')
        os.mkdir(user_dir)

    response = FolderContent(folders=[], files=[])
    for file_or_folder in os.scandir(user_dir):
        if file_or_folder.is_dir():
            response.folders.append(file_or_folder.name)
        else:
            response.files.append(FileInfo(name=file_or_folder.name))

    return response



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
