import datetime
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import Self, Any

class FileModel(BaseModel):
    Key: str
    LastModified: Optional[datetime]
    Size: Optional[int]
class FileMetadata(BaseModel):
    file_name: str
    date: str
    last_modified: str
    size: str
    content_type: str

    @staticmethod
    def get_file_size(content_length: str) -> str:
        size = float(content_length) / 1024
        return f"{size:.2f} KB"

    @classmethod
    def from_http_headers(cls, file_name: str, http_headers: dict[str, Any]) -> Self:
        return cls(
            file_name=file_name,
            date=http_headers["date"],
            last_modified=http_headers["last-modified"],
            size=cls.get_file_size(http_headers["content-length"]),
            content_type=http_headers["content-type"],
        )
