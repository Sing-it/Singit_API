from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from .base_class import Base

DEFAULT_ARTIST_IMAGE = "https://image.shutterstock.com/image-vector/user-icon-trendy-flat-style-260nw-418179865.jpg"  # 추후 AWS S3 url로 수정, schema 파일로 이동


class Artist(Base):
    name = Column(String(50), nullable=False)
    introduction = Column(String(500), nullable=True)
    profile_image = Column(Text, default=DEFAULT_ARTIST_IMAGE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    org_artist = relationship("OrgArtist", uselist=False, back_populates="Artist")

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
    artist_id = Column(Integer, ForeignKey("Artist.id", ondelete="CASCADE"))

    artist = relationship(
        "Artist", back_populates="OrgArtist"  # Artist-OrgArtist One-to-One relationship
    )

    def __repr__(self) -> str:
        return "<{}(id='{}', artist_id='{}')>".format(
            self.__name__, self.id, self.artist_id
        )


class UserArtist(Base):
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"))

    user = relationship(
        "User", back_populates="UserArtist"  # Artist-UserArtist One-to-One relationship
    )

    def __repr__(self) -> str:
        return "<{}(id='{}', user_id='{}')>".format(
            self.__name__, self.id, self.user_id
        )


class ArtistFollow(Base):
    artist_id = Column(Integer, ForeignKey("Artist.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    artist = relationship(
        "Artist",
        backref=backref("ArtistFollow"),  # Artist-ArtistFollow One-to-Many relationship
    )
    user = relationship(
        "User",
        backref=backref("ArtistFollow"),  # User-ArtistFollow One-to-Many relationship
    )

    def __repr__(self) -> str:
        return "<{}(id='{}', artist_id='{}', user_id='{}', created_at='{}')>".format(
            self.__name__, self.id, self.artist_id, self.user_id, self.created_at
        )
