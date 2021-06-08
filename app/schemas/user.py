from typing import Optional
from pydantic import BaseModel, HttpUrl
from pydantic.networks import EmailStr
from datetime import datetime

from app.core.config import settings


class UserBase(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    profile_image: Optional[HttpUrl] = None
    is_active: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserCreate(UserBase):
    email: EmailStr
    password: str
    nickname: str
    profile_image: Optional[HttpUrl] = settings.DEFAULT_ARTIST_IMAGE


class UserLogin(UserBase):
    email: EmailStr
    password: str


class UserPasswordUpdate(BaseModel):
    org_password = str
    new_password = str
