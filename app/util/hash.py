from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(plain_password: str) -> str:
    """
    비밀번호 암호화
    :param plain_password: 평문 형태의 비밀번호
    """
    return context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    비밀번호 검증
    :param plain_password: 확인할 평문형태의 비밀번호
    :param hashed_password: 확인할 암호화된 비밀번호
    """
    return context.verify(plain_password, hashed_password)
