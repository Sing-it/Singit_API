from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app.model.base_class import Base
from app.model.user import User
from app.model.artist import Artist
from app.core.config import settings


class Song(Base):

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    play = Column(Integer, default=0, nullable=False)
    file_link = Column(String(100), nullable=False)
    profile_image = Column(
        String(100), default=settings.DEFAULT_SONG_PROFILE_IMAGE, nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)

    remake_artist_song = relationship(
        "RemakeArtistSong", backref=backref("Song", uselist=False)
    )
    remake_user_song = relationship(
        "RemakeUserSong", backref=backref("Song", uselist=False)
    )

    def __repr__(self) -> str:
        return "<{}(id='{}', title='{}', description='{}', play='{}', file_link='{}', profile_image='{}', created_at='{}', updated_at='{}' )>".format(
            self.__name__,
            self.id,
            self.title,
            self.description,
            self.play,
            self.file_link,
            self.profile_image,
            self.created_at,
            self.updated_at,
        )


class OrgSong(Base):

    id = Column(Integer, autoincrement=True, primary_key=True)
    song_id = Column(Integer, ForeignKey(Song.id, ondelete="CASCADE"), nullable=False)
    artist_id = Column(
        Integer, ForeignKey(Artist.id, ondelete="CASCADE"), nullable=False
    )
    lyric = Column(Text, nullable=True)

    song = relationship(
        "Song",
        backref=backref(
            "OrgSong", uselist=False
        ),  # OrgSong-Song One-to-One relationship
    )
    artist = relationship(
        "Artist",
        backref=backref("OrgSong"),  # Artist-OrgSong One-to-Many relationship
    )

    def __repr__(self) -> str:
        return "<{}(id='{}', song_id='{}', artist_id='{}', lyric='{}')>".format(
            self.__name__, self.id, self.song_id, self.artist_id, self.lyric[:50]
        )


class RemakeArtistSong(Base):

    id = Column(Integer, autoincrement=True, primary_key=True)
    artist_id = Column(
        Integer,
        ForeignKey(Artist.id, ondelete="SET NULL"),
    )
    org_song_id = Column(Integer, ForeignKey(OrgSong.id, ondelete="SET NULL"))
    song_id = Column(Integer, ForeignKey(Song.id, ondelete="CASCADE"), nullable=False)

    org_song = relationship(
        "OrgSong",
        backref=backref(
            "RemakeArtistSong"
        ),  # OrgSong-RemakeArtistSong One-to-Many relationship
    )
    artist = relationship(
        "Artist",
        backref=backref(
            "RemakeArtistSong"
        ),  # Artist-RemakeArtistSong One-to-Many relationship
    )
    song = relationship(
        "Song",
        backref=backref(
            "RemakeArtistSong", uselist=False
        ),  # Song-RemakeArtistSong One-to-One relationship
    )

    def __repr__(self) -> str:
        return "<{}(id='{}', artist_id='{}', org_song_id='{}', song_id='{}', )>".format(
            self.__name__, self.id, self.artist_id, self.org_song_id, self.song_id
        )


class RemakeUserSong(Base):

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="SET NULL"))
    org_song_id = Column(Integer, ForeignKey(OrgSong.id, ondelete="SET NULL"))
    song_id = Column(Integer, ForeignKey(Song.id, ondelete="CASCADE"), nullable=False)

    org_song = relationship(
        "OrgSong",
        backref=backref(
            "RemakeUserSong"
        ),  # OrgSong-RemakeUserSong One-to-Many relationship
    )
    user = relationship(
        "User",
        backref=backref(
            "RemakeUserSong"
        ),  # User-RemakeUserSong One-to-Many relationship
    )
    song = relationship(
        "Song",
        backref=backref("RemakeUserSong", uselist=False),  # Song-RemakeUserSong One-to-One relationship
    )

    def __repr__(self) -> str:
        return "<{}(id='{}', user_id='{}', org_song_id='{}', song_id='{}', )>".format(
            self.__name__, self.id, self.user_id, self.org_song_id, self.song_id
        )


class SongLike(Base):

    id = Column(Integer, autoincrement=True, primary_key=True)
    song_id = Column(Integer, ForeignKey(Song.id, ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    song = relationship(
        "Song", backref=backref("SongLike")
    )  # Song-SongLike One-to-Many relationship
    user = relationship(
        "User", backref=backref("SongLike")
    )  # User-SongLike One-to-Many relationship

    def __repr__(self) -> str:
        return "<{}(id='{}', song_id='{}', user_id='{}', created_at='{}')>".format(
            self.__name__, self.id, self.user_id, self.created_at
        )
