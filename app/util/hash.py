from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(plain_password: str) -> str:
    return context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return context.verify(plain_password, hashed_password)
