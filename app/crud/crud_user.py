from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.model.user import User
from app.schemas.user import UserCreate, UserPasswordUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserPasswordUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        # in sql: select * from User where email=${email} limit 1;
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=obj_in.password,
            nickname=obj_in.nickname,
            profile_image=obj_in,
            is_active=False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        # login 시 사용

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active


user = CRUDUser(User)
