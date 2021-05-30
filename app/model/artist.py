from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

DEFAULT_ARTIST_IMAGE = "https://image.shutterstock.com/image-vector/user-icon-trendy-flat-style-260nw-418179865.jpg"  # 추후 AWS S3 url로 수정, schema 파일로 이동


class Artist(Base):

    name = Column(String(50), nullable=False)
    introduction = Column(String(500), nullable=True)
    profile_image = Column(Text, default=DEFAULT_ARTIST_IMAGE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    org_artist = relationship("OrgArtist", uselist=False, back_populates="Artist")


class OrgArtist(Base):
    artist_id = Column(Integer, ForeignKey("Artist.id", ondelete="CASCADE"))

    artist = relationship("Artist", back_populates="OrgArtist")


class UserArtist(Base):
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="UserArtist")
