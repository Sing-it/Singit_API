from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.model.base_class import Base

DEFAULT_PROFILE_IMAGE = "https://image.shutterstock.com/image-vector/user-icon-trendy-flat-style-260nw-418179865.jpg"  # 추후 AWS S3 url로 수정, schema 파일로 이동


class User(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(100), nullable=False)
    profile_image = Column(String(100), default=DEFAULT_PROFILE_IMAGE)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return "<{}(id='{}', email='{}', password='{}', nickname='{}', profile_image='{}', is_active='{}'created_at='{}', updated_at='{}')>".format(
            self.__name__,
            self.id,
            self.email,
            self.password,
            self.nickname,
            self.profile_image,
            self.is_active,
            self.created_at,
            self.updated_at,
        )
