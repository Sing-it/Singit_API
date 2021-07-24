from typing import Generator
from app.db.sesson import LocalSession
from sqlalchemy.orm import Session
from fastapi import Depends, Header, HTTPException, status

import jwt
from pydantic import ValidationError


from app import model, crud, schemas
from app.core.config import settings


def get_db() -> Generator:
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), authorization: str = Header(None)
) -> model.User:
    try:
        if authorization.split()[0] not in ("jwt", "JWT"):
            raise HTTPException(400, "credentials required")
        token = authorization.split()[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = schemas.AccessTokenPayload(**payload)

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
