# type: ignore

import psycopg2
import os

class PostgresManager:
    def __init__(self):
        self.conn_params = {
            "host": os.getenv('POSTGRES_HOST'),
            "port": os.getenv('POSTGRES_PORT'),
            "database": os.getenv('POSTGRES_DB'),
            "user": os.getenv('POSTGRES_USER'),
            "password": os.getenv('POSTGRES_PASSWORD')
        }

        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cursor = self.conn.cursor()

            return self.cursor
        except Exception as e:
            print(f'[DATABASE ERROR] Falha ao conectar ou criar cursor: {e}')
            raise RuntimeError(f'Erro crítico de banco de dados: {str(e)}')

    def __exit__(self, exc_type, exc, tb):
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