from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr
from uuid import uuid4

from app import crud, model, schemas
from app.api import dependencies
from app.util.redis import RedisUtil

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.UserBase)
def retrieve(user_id: int, db: Session = Depends(dependencies.get_db)) -> Any:
    """
    특정 사용자 정보 조회
    :param user_id: 사용자 인덱스 번호
    """
    user_obj = crud.user.get(db, id=user_id)

    if not user_obj:
        raise HTTPException(status_code=400, detail="invalid user id")
    return Response(user_obj, status_code=200)


@router.post("/register")
def create_user(
    db: Session = Depends(dependencies.get_db),
    user_in: schemas.UserCreate = Body(...),
) -> Any:
    """
    회원가입 API
    :param user_in: UserCreate 스키마
    :return: UserBase 스키마
    """
    user = crud.user.get_by_email(db, email=user_in.email)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    # DB에 is_active=False인 사용자 계정 생성
    user = crud.user.create(db, obj_in=user_in)

    # redis에 key:value = email:auth_code 형식으로 삽입
    auth_code: str = uuid4()
    rd_client = RedisUtil().add_dataset(user.email, auth_code, exp=180)

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
    return Response({"message": "valid email"}, status_code=200)


# GET /users/email?authenticateEmail=[인증할이메일]
@router.get("/send-email")
def send_auth_mail(email: EmailStr, db: Session = Depends(dependencies.get_db)) -> Any:
    """
    계정 활성화 메일 발송 API
    :param email: 메일을 발송할 이메일 주소
    """
    # 1. 이메일 isvalid
    # 2. 이메일 발송 -> celery 모듈 필요

    user = crud.user.get_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=401, detail="there's no account with email [{}]".format(email)
        )
    is_active: bool = crud.user.is_active(user)
    if is_active:
        raise HTTPException(status_code=401, detail="this account already active")
    # send_mail 모듈 적용


@router.patch("/activate", response_model=schemas.UserBase)
def activate_account(
    db: Session = Depends(dependencies.get_db),
    *,
    email: str = Body(...),
    code: str = Body(...),
) -> Any:
    """
    사용자 계정 활성화 API (회원가입에 사용한 이메일 주소로 보내진 인증코드 확인 후 활성화)
    :param email: 활성화시킬 계정의 이메일 주소
    :param code: 이메일 주소로 보내진 계정 활성화 인증 코드
    """

    user_obj = crud.user.get_by_email(db, email=email)
    if not user_obj:
        raise HTTPException(status_code=400, detail="invalid user email")
    # redis 연동 모듈
    is_authenticate = RedisUtil().check_email_auth_code(email, code)

    if not is_authenticate:
        raise HTTPException(status_code=401, detail="invalid auth code")

    user_obj = crud.user.activate(db, user_obj)
    return Response(user_obj, status_code=201)


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
    return Response({"message": "password update success"}, status_code=201)
