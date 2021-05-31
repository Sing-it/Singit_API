from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from .base import Base

DEFAULT_SONG_PROFILE_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_rB4T2_cyi76yYVELAVqs-pPu3nalV_ZpQA&usqp=CAU"


class Song(Base):
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    play = Column(Integer, default=0)
    file_link = Column(Text, nullable=False)
    profile_image = Column(Text, default=DEFAULT_SONG_PROFILE_IMAGE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    remake_artist_song = relationship(
        "RemakeArtistSong", uselist=False, back_populates="Song"
    )
    remake_user_song = relationship(
        "RemakeUserSong", uselist=False, back_populates="Song"
    )


class OrgSong(Base):
    song_id = Column(Integer, ForeignKey("Song.id", ondelete="CASCADE"), nullable=False)
    artist_id = Column(
        Integer, ForeignKey("Artist.id", ondelete="CASCADE"), nullable=False
    )
    lyric = Column(Text, nullable=True)

    song = relationship(
        "Song",
        backref=backref(
            "OrgSong", uselist=False
        ),  # OrgSong-Song One-to-One relationship
    )
    artist = relationship(
        "Artist", backref=backref("OrgSong")  # Artist-OrgSong One-to-Many relationship
    )


class RemakeArtistSong(Base):
    artist_id = Column(Integer, ForeignKey("Artist.id", ondelete="SET NULL"))
    org_song_id = Column(Integer, ForeignKey("OrgSong.id", ondelete="SET NULL"))
    song_id = Column(Integer, ForeignKey("Song.id", ondelete="CASCADE"), nullable=False)

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
        back_populates="RemakeArtistSong",  # Song-RemakeArtistSong One-to-One relationship
    )


class RemakeUserSong(Base):
    user_id = Column(Integer, ForeignKey("User.id", ondelete="SET NULL"))
    org_song_id = Column(Integer, ForeignKey("OrgSong.id", ondelete="SET NULL"))
    song_id = Column(Integer, ForeignKey("Song.id", ondelete="CASCADE"), nullable=False)

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
        back_populates="RemakeUserSong",  # Song-RemakeUserSong One-to-One relationship
    )


class SongLike(Base):
    song_id = Column(Integer, ForeignKey("Song.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    song = relationship(
        "Song", backref=backref("SongLike")
    )  # Song-SongLike One-to-Many relationship
    user = relationship(
        "User", backref=backref("SongLike")
    )  # User-SongLike One-to-Many relationship
