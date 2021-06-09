from typing import Optional, List
from pydantic import BaseModel, HttpUrl

from app.schemas.song import SongBase


class PlaylistBase(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    owner_id: Optional[int] = None
    profile_image: Optional[HttpUrl] = None
    like: Optional[int] = 0


class PlaylistCreate(PlaylistBase):
    title: str
    profile_image: str


class PlaylistDetail(PlaylistBase):
    id: int
    title: str
    owner_id: int
    profile_image: HttpUrl
    like: int
    songs: Optional[List[SongBase]] = None


class PlaylistList(PlaylistBase):
    results: Optional[List[PlaylistBase]]
