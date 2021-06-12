from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from pydantic.networks import EmailStr


class Token(BaseModel):
    token: str


class AccessTokenPayload(BaseModel):
    exp: datetime
    iat: datetime
    sub: int
    email: EmailStr
    hash_password: str


class RefreshTokenPayload(BaseModel):
    exp: datetime
    iat: datetime
