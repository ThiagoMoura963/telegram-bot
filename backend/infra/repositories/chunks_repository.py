from psycopg2.extras import execute_values

from backend.infra.database import PostgresManager


class ChunksRepository:
    def __init__(self):
        self.postgres_manager = PostgresManager()

    def save_all(self, document_id, chunks_data, user_id, agent_id):
        sql = 'INSERT INTO app.document_chunks (document_id, user_id, agent_id, content, content_vector) VALUES %s'

        values = [(document_id, user_id, agent_id, chunk, list(vector)) for chunk, vector in chunks_data]

        try:
            with self.postgres_manager as cursor:
                execute_values(cursor, sql, values)

        except Exception as e:
            raise RuntimeError(f'Erro ao inserir chunks em lote: {e}') from e

    def find_similiar_chunk(self, query_embedding, agent_id, limit=5):
        sql = (
            'SELECT d.file_name, dc.content '
            'FROM app.document_chunks dc '
            'INNER JOIN app.documents d ON d.id = dc.document_id '
            'WHERE dc.agent_id = %s '
            'ORDER BY dc.content_vector <=> %s::vector '
            'LIMIT %s;'
        )

        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, (agent_id, list(query_embedding), limit))
                rows = cursor.fetchall()

                return [{'source': row[0], 'content': row[1]} for row in rows]

        except Exception as e:
            raise RuntimeError(f'Erro ao buscar chunks similares: {e}') from e
