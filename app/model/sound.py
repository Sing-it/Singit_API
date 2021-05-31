from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

from .base import Base


class UserSound(Base):
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"))
    lyric = Column(Text, nullable=False)
    song_melody = Column(Text, nullable=False)  # song melody sound file url
    sound = Column(Text, nullable=False)  # user's sound file url

    user = relationship(
        "User", backref=backref("UserSound")
    )  # User-UserSound One-to-Many relationship
