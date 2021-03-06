from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app.model.base_class import Base
from app.model.user import User
from app.core.config import settings


class Artist(Base):

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    introduction = Column(String(500), nullable=True)
    profile_image = Column(
        String(100), default=settings.DEFAULT_ARTIST_IMAGE, nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return "<{}(id='{}', name='{}', introduction='{}', profile_image='{}', created_at='{}', updated_at='{}')>".format(
            self.__name__,
            self.id,
            self.name,
            self.introduction,
            self.profile_image,
            self.created_at,
            self.updated_at,
        )


class OrgArtist(Base):

    id = Column(Integer, autoincrement=True, primary_key=True)
    artist_id = Column(
        Integer, ForeignKey(Artist.id, ondelete="CASCADE"), nullable=False
    )

    artist = relationship(
        "Artist",
        backref=backref(
            "OrgArtist", uselist=False
        ),  # Artist-OrgArtist One-to-One relationship
    )

    def __repr__(self) -> str:
        return "<{}(id='{}', artist_id='{}')>".format(
            self.__name__, self.id, self.artist_id
        )


class UserArtist(Base):

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)

    user = relationship(
        "User",
        backref=backref(
            "UserArtist", uselist=False
        ),  # User-UserArtist One-to-One relationship
    )

    def __repr__(self) -> str:
        return "<{}(id='{}', user_id='{}')>".format(
            self.__name__, self.id, self.user_id
        )


class ArtistFollow(Base):

    artist_id = Column(
        Integer, ForeignKey(Artist.id, ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), primary_key=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    artist = relationship(
        "Artist",
        backref=backref("ArtistFollow"),  # Artist-ArtistFollow One-to-Many relationship
    )
    user = relationship(
        "User",
        backref=backref("ArtistFollow"),  # User-ArtistFollow One-to-Many relationship
    )

    def __repr__(self) -> str:
        return "<{}( artist_id='{}', user_id='{}', created_at='{}')>".format(
            self.__name__, self.artist_id, self.user_id, self.created_at
        )
