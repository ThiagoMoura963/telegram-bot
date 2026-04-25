from ..database import PostgresManager


class DocumentRepository:
    def __init__(self):
        self.postgres_manager = PostgresManager()

    def get_all(self, user_id, agent_id):
        sql = (
            'SELECT DISTINCT d.id, d.file_name, d.created_at '
            'FROM app.documents d '
            'INNER JOIN app.document_chunks dc ON dc.document_id = d.id '
            'WHERE dc.user_id = %s AND dc.agent_id = %s'
            'ORDER BY d.created_at DESC;'
        )

        try:
            with self.postgres_manager as cursor:
                cursor.execute(
                    sql,
                    (
                        user_id,
                        agent_id,
                    ),
                )
                rows = cursor.fetchall()

                return [
                    {
                        'id': str(row[0]),
                        'file_name': row[1],
                        'created_at': row[2].isoformat(),
                    }
                    for row in rows
                ]
        except Exception as e:
            raise RuntimeError(f'Erro ao buscar documentos: {e}') from e

    def save(self, file_name):
        sql = 'INSERT INTO app.documents (file_name) VALUES (%s) RETURNING id;'

        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, (file_name,))
                row = cursor.fetchone()

                if row is None:
                    raise Exception('[ERROR] Falha ao inserir documento.')

                document_id = row[0]

                if document_id is None:
                    raise Exception('[ERROR] ID do document não retornado.')

                return document_id
        except Exception as e:
            raise RuntimeError(f'Erro ao inserir documento: {e}') from e
