from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship, backref

from app.model.base_class import Base
from app.model.user import User
from app.model.artist import OrgArtist


class RemakeMaterial(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100), nullable=False)
    artist = Column(String(50), nullable=False)  # artist name
    song = Column(String(100), nullable=False)  # song File URL
    accompaniment = Column(String(100), nullable=False)  # accompaniment File URL
    lyric = Column(String(200), nullable=True)

    def __repr__(self) -> str:
        return "<{}(id='{}', title='{}', artist='{}', song='{}', accompaniment='{}', lyric='{}')>".format(
            self.__name__,
            self.id,
            self.title,
            self.artist,
            self.song,
            self.accompaniment,
            self.lyric[:50],
        )


class UserSound(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    sound = Column(String(100), nullable=False)  # user's file url
    material_id = Column(Integer, ForeignKey(RemakeMaterial.id, ondelete="CASCADE"))

    user = relationship(
        "User", backref=backref("UserSound")
    )  # User-UserSound One-to-Many relationship

    material = relationship(
        "RemakeMaterial", backref=backref("UserSound")
    )  # RemakeMaterial-User One-to-Many relationship

    def __repr__(self) -> str:
        return "<{}(id='{}', user_id='{}', lyric='{}', song_melody='{}', sound='{}')>".format(
            self.__name__,
            self.id,
            self.user_id,
            self.lyric[:50],
            self.song_melody,
            self.sound,
        )


class ArtistSound(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    artist_id = Column(Integer, ForeignKey(OrgArtist.id, ondelete="SET_NULL"))
    song = Column(String(100), nullable=False)  # song File URL
    sound = Column(String(100), nullable=False)  # artist's file url
    lyric = Column(String(200), nullable=True)


    def __repr__(self) -> str:
        return "<{}(id='{}', user_id='{}', lyric='{}', song_melody='{}', sound='{}')>".format(
            self.__name__,
            self.id,
            self.user_id,
            self.lyric[:50],
            self.song_melody,
            self.sound,
        )
