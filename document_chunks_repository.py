import config
from database import PostgresManager
from psycopg2 import Error
from psycopg2.extras import execute_values

class DocumentChunksRepository:
    def __init__(self):
        self.db_manager = PostgresManager(
            config.POSTGRES_USERNAME,
            config.POSTGRES_PASSWORD,
            config.POSTGRES_HOST,
            config.POSTGRES_PORT,
            config.POSTGRES_DATABASE
        )

    def bulk_insert(self, document_id: str, chunks_data: list[tuple]):
        sql = 'INSERT INTO app.document_chunks (document_id, content, content_vector, sequence_id) VALUES %s'
        
        values = [(document_id, data[0], data[1], data[2]) for data in chunks_data]
        
        try:
            with self.db_manager as cur:
                execute_values(cur, sql, values)
                print(f"Inseridos {cur.rowcount} chunks em lote para o documento ID: {document_id}")
                
        except Error as e:
            print(f'Erro ao inserir chunks em lote: {e}')
