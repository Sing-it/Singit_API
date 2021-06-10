import json
from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, model, schemas
from app.api import dependencies


router = APIRouter()


@router.post("/register")
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(dependencies.get_db()),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)  # get_by_email 구현
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return JSONResponse(
        {"message": "Please check your email to activate your account"}, status_code=201
    )

