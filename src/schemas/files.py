from pydantic import BaseModel


class FileInfo(BaseModel):
    name: str


class FolderContent(BaseModel):
    folders: list[str] | None
    files: list[FileInfo] | None
