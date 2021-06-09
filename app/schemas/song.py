from typing import Optional
from pydantic import BaseModel, HttpUrl


class SongBase(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    artist_id: Optional[int] = None
    description: Optional[str] = None
    play: Optional[int] = None
    link: Optional[HttpUrl] = None
    profile_image: Optional[HttpUrl] = None


