from pydantic import BaseModel
from datetime import datetime

class ImageOut(BaseModel):
    id: int
    filename: str
    url: str
    size: int
    created_at: datetime

    class Config:
        from_attributes = True

class ImageList(BaseModel):
    items: list[ImageOut]
    total: int