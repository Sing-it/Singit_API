from typing import Optional, List
from pydantic import BaseModel, HttpUrl

from app.schemas.artist import ArtistResultDetail


class MaterialBase(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    artist: Optional[str] = None
    song: Optional[HttpUrl] = None
    accompaniment: Optional[HttpUrl] = None
    lyric: Optional[str] = None


class ArtistSoundBase(BaseModel):
    id: Optional[int] = None
    artist_id: Optional[int] = None
    song: Optional[HttpUrl] = None
    accompaniment: Optional[HttpUrl] = None
    lyric: Optional[str] = None


class ArtistSoundList(BaseModel):
    results: Optional[List[ArtistResultDetail]]


class MaterialBaseResult(MaterialBase):
    id: int
    title: str
    artist: str
    accompaniment: HttpUrl
    lyric: str


class MaterialList(MaterialBase):
    results: Optional[List[MaterialBaseResult]]
