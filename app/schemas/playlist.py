from typing import Optional, List
from pydantic import BaseModel, HttpUrl

from app.schemas.song import SongBaseResult
from app.core.config import settings


class PlaylistBase(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    owner_id: Optional[int] = None
    profile_image: Optional[HttpUrl] = None
    like: Optional[int] = 0


class PlaylistBaseResult(PlaylistBase):
    id: int
    title: str
    owner_id: int
    profile_image: HttpUrl
    like: int = 0


class PlaylistCreate(PlaylistBase):
    title: str
    profile_image: HttpUrl = settings.DEFAULT_SONG_PROFILE_IMAGE


class PlaylistDetail(PlaylistBase):
    id: int
    title: str
    owner_id: int
    profile_image: HttpUrl
    like: int = 0
    songs: Optional[List[SongBaseResult]] = None


class PlaylistList(PlaylistBase):
    results: Optional[List[PlaylistBaseResult]]
