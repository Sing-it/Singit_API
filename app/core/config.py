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

    SQLALCHEMY_DATABASE_URI: str = (
        "mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8".format(
            DB_USER,
            DB_PASSWORD,
            DB_HOST,
            DB_PORT,
            DB_NAME,
        )
    )
    DEFAULT_SONG_PROFILE_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_rB4T2_cyi76yYVELAVqs-pPu3nalV_ZpQA&usqp=CAU"  # 추후 AWS S3 url로 수정, schema 파일로 이동
    DEFAULT_ARTIST_IMAGE = "https://image.shutterstock.com/image-vector/user-icon-trendy-flat-style-260nw-418179865.jpg"  # 추후 AWS S3 url로 수정, schema 파일로 이동
    DEFAULT_PROFILE_IMAGE = "https://image.shutterstock.com/image-vector/user-icon-trendy-flat-style-260nw-418179865.jpg"  # 추후 AWS S3 url로 수정, schema 파일로 이동

    AWS_CONFIG = {
        "REGION": os.getenv("REGION"),
        "ACCESS_KEY_ID": os.getenv("ACCESS_KEY_ID"),
        "SECRET_KEY": os.getenv("SECRET_KEY"),
        "BUCKET_NAME": os.getenv("BUCKET_NAME"),
    }


settings = Settings()
