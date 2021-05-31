from typing import Generator
from app.db.sesson import LocalSession


def get_db() -> Generator:
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()
