from psycopg2 import Error
from database import PostgresManager
import config

class DocumentRespository:
    def __init__(self):
        self.db_manager = PostgresManager(
            config.POSTGRES_USERNAME,
            config.POSTGRES_PASSWORD,
            config.POSTGRES_HOST,
            config.POSTGRES_PORT,
            config.POSTGRES_DATABASE
        )

    def create(self, file_name):
        sql = 'INSERT INTO app.documents (file_name) VALUES (%s) RETURNING id'
        document_id = None

        try:
            with self.db_manager as cur:
                cur.execute(sql, (file_name,))
                document_id = cur.fetchone()[0]
                print(f"Documento '{file_name}' inserido com ID: {document_id}")
<<<<<<< HEAD

        except Error as e:
            print(f'Erro ao inserir documento: {e}')

        return document_id
=======
        except Error as e:
            print(f'Erro ao inserir documento: {e}')

        return document_id
>>>>>>> recuperado
