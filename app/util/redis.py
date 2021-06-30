from typing import Any
import redis

from app.core.config import settings


class RedisUtil:
    def __init__(self) -> None:
        self.redis_client = redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
        )

    def delete_set(self, key: str) -> Any:
        return self.redis_client.delete(key)

    def get_set(self, key: str) -> Any:
        return self.redis_client.get(key)

    def add_dataset(self, key: str, value: str) -> Any:
        return self.redis_client.set(key, value)

    def flush_db(self) -> Any:
        return self.redis_client.flushdb()

    def check_email_auth_code(self, email: str, code: int) -> bool:
        return self.get_set(email) == code
