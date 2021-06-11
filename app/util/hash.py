from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(plain_password: str) -> str:
    return context.hash(plain_password)
