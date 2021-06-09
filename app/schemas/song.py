from typing import Optional, List
from pydantic import BaseModel, HttpUrl


class SongBase(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    artist_id: Optional[int] = None
    description: Optional[str] = None
    play: Optional[int] = None
    like: Optional[int] = None
    link: Optional[HttpUrl] = None
    profile_image: Optional[HttpUrl] = None


class SongBaseResult(SongBase):
    id: int
    title: str
    artist_id: int
    play: int = 0
    like: int = 0
    profile_image: HttpUrl


class SongList(SongBase):
    results: Optional[List[SongBaseResult]] = None
