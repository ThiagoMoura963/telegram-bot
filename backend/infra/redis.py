import os
from typing import Optional

import redis
from dotenv import load_dotenv

load_dotenv()


class RedisManager:
    def __init__(self):
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = os.getenv('REDIS_PORT', 6379)
        self.db = int(os.getenv('REDIS_DB', 0))
        self._client: Optional[redis.Redis] = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.Redis(
                host=self.host or 'localhost',
                port=self.port or 6379,
                db=self.db or 0,
                decode_responses=True,
            )

            try:
                self._client.ping()
            except Exception:
                print('[REDIS ERROR] Redis não detectado na inicialização.')

        return self._client


redis_manager = RedisManager()
