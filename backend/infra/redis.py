import os
from typing import Optional

import redis
from dotenv import load_dotenv

load_dotenv()


class RedisManager:
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL')

        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.db = int(os.getenv('REDIS_DB', 0))

        self._client: Optional[redis.Redis] = None

    @property
    def client(self) -> Optional[redis.Redis]:
        if self._client is None:
            try:
                if self.redis_url:
                    self._client = redis.from_url(
                        self.redis_url,
                        decode_responses=True,
                    )
                else:
                    self._client = redis.Redis(
                        host=self.host,
                        port=self.port,
                        db=self.db,
                        decode_responses=True,
                    )

                self._client.ping()
                print('[REDIS] Redis conectado com sucesso.')

            except Exception as e:
                print(f'[REDIS ERROR] Redis não detectado: {e}')
                self._client = None

        return self._client


redis_manager = RedisManager()