from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref

from .base_class import Base


class PlayList(Base):
    title = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("User.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship(
        "User", backref=backref("PlayList")
    )  # User-PlayList One-to-Many relationship

    def __repr__(self) -> str:
        return "<{}(id='{}', title='{}', user_id='{}', created_at='{}', updated_at='{}')>".format(
            self.__name__,
            self.id,
            self.title,
            self.user_id,
            self.created_at,
            self.updated_at,
        )


class PlayListSong(Base):
    playlist_id = Column(Integer, ForeignKey("PlayList.id", ondelete="CASCADE"))
    song_id = Column(Integer, ForeignKey("Song.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    playlist = relationship(
        "PlayList", backref=backref("PlayListSong")
    )  # PlayList-PlayListSong One-to-Many relationship
    song = relationship(
        "Song", backref=backref("PlayListSong")
    )  # Song-PlayListSong One-to-Many relationship

    def __repr__(self) -> str:
        return "<{}(id='{}', playlist_id='{}', song_id='{}', created_at='{}')>".format(
            self.__name__, self.id, self.artist_id, self.song_id, self.created_at
        )


class PlayListLike(Base):
    playlist_id = Column(Integer, ForeignKey("PlayList.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    playlist = relationship(
        "PlayList", backref=backref("PlayListLike")
    )  # PlayList-PlayListSong One-to-Many relationship
    user = relationship(
        "User", backref=backref("PlayListLike")
    )  # User-PlayListSong One-to-Many relationship

    def __repr__(self) -> str:
        return "<{}(id='{}', playlist_id='{}', user_id='{}', created_at='{}')>".format(
            self.__name__, self.id, self.playlist_id, self.user_id, self.created_at
        )
