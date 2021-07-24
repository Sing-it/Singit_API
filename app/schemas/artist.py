from typing import Optional
from pydantic import BaseModel, HttpUrl


class ArtistBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    introduction: Optional[str] = None
    profile_image: Optional[HttpUrl] = None
    follow: Optional[int] = 0


class ArtistResultBase(ArtistBase):
    id: int
    name: str
    profile_image: HttpUrl
    follow: int = 0


class ArtistResultDetail(ArtistBase):
    id: int
    name: str
    profile_image: HttpUrl
    introduction: Optional[str]
    follow: int = 0
