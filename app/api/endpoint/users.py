import json
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr

from app import crud, model, schemas
from app.api import dependencies


router = APIRouter()


@router.post("/register")
def create_user(
    db: Session = Depends(dependencies.get_db),
    user_in: schemas.UserCreate = Body(...),
) -> Any:
    """
    회원가입 API
    :param user_in: UserCreate 스키마
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
def check_email(email: EmailStr, db: Session = Depends(dependencies.get_db)) -> Any:
    """
    이메일 중복 체크 API
    :param email: 중복 체크할 이메일
    """
    user = crud.user.get_by_email(db, email)
    if user:
        raise HTTPException(status_code=401, detail="email already exists.")
    return Response(
        json.dumps({"message": "valid email"}),
        status_code=200,
        media_type="application/json",
    )


@router.get("/reset-password")
def reset_password(
    db: Session = Depends(dependencies.get_db),
    *,
    obj_in: schemas.UserPasswordUpdate,
    current_user: model.User = Depends(dependencies.get_current_user),
) -> Any:
    """
    비밀번호 재설정 API
    """
    user = crud.user.authenticate(db, current_user.email, current_user.password)
    if not user:
        raise HTTPException(status_code=401, detail="wrong password")
    crud.user.update(
        db, db_obj=current_user, obj_in=obj_in
    )  # crud에 password 없데이트 기능 추가하기
    return Response({"msg": "password update success"}, status_code=201)
