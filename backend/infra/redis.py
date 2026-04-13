import redis
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class RedisManager:
    def __init__(self):
        self.host = os.getenv('REDIS_HOST')
        self.port = os.getenv('REDIS_PORT')
        self.db = int(os.getenv('REDIS_DB', 0))
        self._client: Optional[redis.Redis] = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            try:
                self._client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    decode_responses=True
                )
                self._client.ping()
            except Exception as e:
                print(f'[REDIS ERROR] Falha ao conectar ao Redis: {e}')
                raise RuntimeError(f'Erro crítico de cache: {str(e)}') from e
        return self._client

redis_manager = RedisManager()
