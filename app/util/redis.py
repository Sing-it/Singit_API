from typing import Any
import redis
from datetime import timedelta

from app.core.config import settings


class RedisUtil:
    def __init__(self) -> None:
        self.redis_client = redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
        )

    def delete_set(self, key: str) -> Any:
        """
        특정 데이터셋 삭제 모듈
        :param key: 삭제할 데이터의 Key
        """
        return self.redis_client.delete(key)

    def get_set(self, key: str) -> Any:
        """
        특정 데이터셋 조회 모듈
        :param key: 조회할 데이터의 Key
        """
        return self.redis_client.get(key)

    def add_dataset(self, key: str, value: str, *exp: int) -> Any:
        """
        특정 데이터 셋 추가
        :param key: 추가할 데이터의 Key
        :param value: 추가할 데이터의 Value
        :*param exp: 데이터의 만료시간
        """
        if exp:
            return self.redis_client.set(key, value, timedelta(seconds=exp))
        return self.redis_client.set(key, value)

    def flush_db(self) -> Any:
        """
        Redis DB 초기화
        """
        return self.redis_client.flushdb()

    def check_email_auth_code(self, email: str, code: int) -> bool:
        """
        이메일 인증 코드 확인
        :param email: 확인할 Key 값
        :param code: 확인할 인증번호
        """
        return self.get_set(email) == code
