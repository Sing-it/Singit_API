from typing import Any
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str
    id = Column(Integer, autoincrement=True, primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__
