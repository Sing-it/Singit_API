import json
from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, Response
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
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)

    return Response(
        {"message": "Please check your email to activate your account"}, status_code=201
    )


@router.get("/email")
def check_email(email: str, db: Session = Depends(dependencies.get_db())) -> Any:
    """
    이메일 중복 체크 API
    :param email: 중복 체크할 이메일
    """
    user = crud.user.get_by_email(db, email)
    if user:
        raise HTTPException(status_code=401, detail="email already exists.")
    return Response({"message": "valid email"}, status_code=200)
