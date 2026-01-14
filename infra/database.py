import psycopg2
from psycopg2 import Error
from psycopg2.extensions import connection, cursor
from contextlib import AbstractContextManager
from typing import Any


class PostgresManager(AbstractContextManager[cursor]):
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: str,
        database: str
    ):
        self.conn_params: dict[str, Any] = {
            'user': username,
            'password': password,
            'host': host,
            'port': port,
            'database': database,
        }

        self.conn: connection | None = None
        self.cursor: cursor | None = None

    def __enter__(self) -> cursor:
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            cur = self.conn.cursor()
            self.cursor = cur
            return cur
        except Error as e:
            raise RuntimeError('Falha ao conectar ao PostgreSQL') from e

    def __exit__(self, exc_type, exc, tb) -> bool:
        try:
            if self.conn:
                if exc_type:
                    self.conn.rollback()
                else:
                    self.conn.commit()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

        return False
