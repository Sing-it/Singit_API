import secrets
import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SERVER_PORT: int = os.getenv("SERVER_PORT")
    SERVER_HOST: str = os.getenv("SERVER_HOST")

    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY") or secrets.token_urlsafe(32)
    ALGORITHM: str = os.getenv("JWT_ALGORITHM")

    MODE: bool = os.getenv("MODE")

    # Database Setting
    DB_HOST: str = os.getenv("LOCAL_DB_HOST") if MODE else os.getenv("RDS_DB_HOST")
    DB_USER: str = os.getenv("LOCAL_DB_USER") if MODE else os.getenv("RDS_DB_USER")
    DB_PASSWORD: str = (
        os.getenv("LOCAL_DB_PASSWORD") if MODE else os.getenv("RDS_DB_PASSWORD")
    )
    DB_NAME: str = os.getenv("LOCAL_DB_NAME") if MODE else os.getenv("RDS_DB_NAME")
    DB_PORT: str = os.getenv("LOCAL_DB_PORT") if MODE else os.getenv("RDS_DB_PORT")

    SQLALCHEMY_DATABASE_URI: str = "mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8".format(
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )


settings = Settings()
