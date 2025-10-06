import psycopg2
from psycopg2 import Error
from psycopg2.extensions import connection, cursor as Cursor
from pgvector.psycopg2 import register_vector

class PostgresManager:
    def __init__(self, username, password, host, port, database):
        self.conn_params = {
            "user": username,
            "password": password,
            "host": host,
            "port": port,
            "database": database
        }
        self.conn: connection | None = None
        self.cursor: Cursor | None = None
        
    def __enter__(self) -> Cursor:
        try:
            self.conn = psycopg2.connect(**self.conn_params)

            register_vector(self.conn)

            self.cursor = self.conn.cursor()
            print('Conectado no banco postgres com sucesso.')
            return self.cursor
        except Error as e:
           print(f'Ocorreu um erro ao se conectar com o banco de dados: {e}')
    
    def __exit__(self, class_except, except_, traceback_):
        if class_except is not None:
            print(f"Ocorreu um erro na transação: {except_}. Executando rollback.")
            print(traceback_)
            self.conn.rollback()
        else:
            print('Transação bem-sucedida. Executando commit.')
            self.conn.commit()

        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print('Conexão com o banco de dados encerrada.')
        
        return False