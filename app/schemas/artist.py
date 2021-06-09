from typing import Optional
from pydantic import BaseModel, HttpUrl


class ArtistBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    introduction: Optional[str] = None
    profile_image: Optional[HttpUrl] = None
    follow: Optional[int] = None


class ArtistResultBase(ArtistBase):
    id: str
    name: str
    profile_image: HttpUrl
    follow: int
