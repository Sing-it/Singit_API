from typing import Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime


class ArtistBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    introduction: Optional[str] = None
    profile_image: Optional[HttpUrl] = None
    created_at = Optional[datetime]
    updated_at = Optional[datetime]


class ArtistOutput(ArtistBase):
    id: str
    name: str
    introduction: Optional[str] = None
    profile_image: HttpUrl
