from typing import Optional, List
from pydantic import BaseModel

from app.schemas.playlist import PlaylistBaseResult
from app.schemas.artist import ArtistResultBase
from app.schemas.song import SongBaseResult


class SearchPlaylist(BaseModel):
    results: Optional[List[PlaylistBaseResult]]


class SearchArtist(BaseModel):
    results: Optional[List[ArtistResultBase]]


class SearchSong(BaseModel):
    results: Optional[List[SongBaseResult]]
