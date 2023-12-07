from fastapi import APIRouter, File, UploadFile


router = APIRouter(
    prefix="/files",
    tags=["files"],
)



