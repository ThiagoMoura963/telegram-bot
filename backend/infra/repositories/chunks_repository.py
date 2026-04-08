from backend.infra.database import PostgresManager
from psycopg2.extras import execute_values

class ChunksRepository:
    def __init__(self):
        self.postgres_manager = PostgresManager()

    def save_all(self, document_id, chunks_data):
        sql = 'INSERT INTO app.document_chunks ' \
        '(document_id, content, content_vector) VALUES %s'

        values = [
            (document_id, chunk, list(vector))
            for chunk, vector in chunks_data
        ]
        try:
            with self.postgres_manager as cursor:
                execute_values(cursor, sql, values)
        except Exception as e :
            raise RuntimeError("Erro ao inserir chunks em lote:", e)
    
    def find_similiar_chunk(self, query_embedding, limit=5):
        sql = 'SELECT d.file_name AS source, dc.content FROM app.document_chunks dc INNER JOIN app.documents d ON d.id = dc.document_id ORDER BY dc.content_vector <=> %s::vector LIMIT %s;'

        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, (list(query_embedding), limit))
                rows = cursor.fetchall()

                return [{'source': row[0], 'content': row[1]} for row in rows]
        except Exception as e:
            raise RuntimeError(f'Erro ao buscar chunks similares: {e}')