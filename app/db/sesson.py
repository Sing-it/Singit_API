from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
LocalSession = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # flush:(insert, update, delete) 작업 관련. 즉, commit의 일부분
