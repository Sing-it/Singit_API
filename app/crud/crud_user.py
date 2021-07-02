from typing import Optional, Dict, Union, Any

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update

from app.crud.base import CRUDBase
from app.model.user import User
from app.schemas.user import UserCreate, UserPasswordUpdate
from app.util import s3upload, get_hashed_password, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserPasswordUpdate]):
    def get(self, db: Session, id: int):
        """
        index값을 통한 사용자 계정 존재 여부 확인
        """
        # in sql: select * from User where id=${id} limit 1;
        return db.query(User).filter(User.id == id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        이메일을 통한 사용자 계정 존재 여부 확인
        """
        # in sql: select * from User where email=${email} limit 1;
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        """
        사용자 계정 초기 생성(비활성화 상태)
        """
        # in sql: insert into User(email, password, nickname, profile_image, is_active) values({email}, {password}, {nickname}, {profile_image}, False)
        db_obj = User(
            email=obj_in.email,
            password=get_hashed_password(obj_in.password),
            nickname=obj_in.nickname,
            profile_image=obj_in.profile_image,
            is_active=False,
        )
        save_change(db, db_obj)
        return db_obj

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        """
        이메일, 비밀번호 일치 여부 확인
        :param email: 확인할 이메일
        :param password: 확인할 비밀번호
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserPasswordUpdate, Dict[str, Any]]
    ) -> User:
        """
        사용자 계정 정보 수정
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_hashed_password(update_data["new_password"])
            del update_data["new_password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_active(self, user: User) -> bool:
        """
        사용자 계정 활성화 여부 확인
        """
        return user.is_active

    def activate(self, db: Session(), user: User) -> Any:
        """
        사용자 계정 활성화
        """
        if self.is_active(user):
            return "Already active email"
        update_data = {"is_active": True}
        return super().update(db, db_obj=user, obj_in=update_data)


user = CRUDUser(User)


def save_change(db: Session, data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        raise e
