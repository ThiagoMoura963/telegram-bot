from ..database import PostgresManager


class DocumentRepository:
    def __init__(self):
        self.postgres_manager = PostgresManager()

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
