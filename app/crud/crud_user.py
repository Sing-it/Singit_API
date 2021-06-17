from typing import Optional, Dict, Union, Any

from sqlalchemy.orm import Session
from datetime import datetime
from calendar import timegm
from app.crud.base import CRUDBase
from app.model.user import User
from app.schemas.user import UserCreate, UserPasswordUpdate
from app.util import s3upload, get_hashed_password, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserPasswordUpdate]):
    def get(self, db: Session, id: int):
        # in sql: select * from User where id=${id} limit 1;
        return db.query(User).filter(User.id == id)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        # in sql: select * from User where email=${email} limit 1;
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        filename = obj_in.email + "_" + str(timegm(datetime.utcnow().utctimetuple())) + '.png'
        obj_img_url = s3upload(
            file=obj_in.profile_image, path="image/user/", filename=filename
        )
        db_obj = User(
            email=obj_in.email,
            password=get_hashed_password(obj_in.password),
            nickname=obj_in.nickname,
            profile_image=obj_img_url,
            is_active=False,
        )
        save_change(db, db_obj)
        return db_obj

    # 로그인 시 사용
    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
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
        return user.is_active


user = CRUDUser(User)


def save_change(db: Session, data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        raise e
