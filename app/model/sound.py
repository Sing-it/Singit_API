from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

from .base_class import Base


class UserSound(Base):
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"))
    lyric = Column(Text, nullable=False)
    song_melody = Column(Text, nullable=False)  # song melody sound file url
    sound = Column(Text, nullable=False)  # user's sound file url

    user = relationship(
        "User", backref=backref("UserSound")
    )  # User-UserSound One-to-Many relationship

    def __repr__(self) -> str:
        return "<{}(id='{}', user_id='{}', lyric='{}', song_melody='{}', sound='{}')>".format(
            self.__name__, self.id, self.user_id, self.lyric[:50], self.song_melody, self.sound
        )
