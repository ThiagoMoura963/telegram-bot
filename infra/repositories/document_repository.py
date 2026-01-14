from psycopg2 import Error
from ..database import PostgresManager
import config

class DocumentRepository:
    def __init__(self) -> None:
        self.db_manager = PostgresManager(
            str(config.POSTGRES_USERNAME),
            str(config.POSTGRES_PASSWORD),
            str(config.POSTGRES_HOST),
            str(config.POSTGRES_PORT),
            str(config.POSTGRES_DATABASE)
        )

    def create(self, file_name: str) -> int:
        sql = 'INSERT INTO app.documents (file_name) VALUES (%s) RETURNING id'

        doc_id: int | None = None
        
        try:
            with self.db_manager as cur:
                assert cur is not None

                cur.execute(sql, (file_name,))
                row = cur.fetchone()

                if row is None:
                    raise RuntimeError('Falha ao inserir documento')
                
                if row:
                    doc_id = row[0]
            
            if doc_id is None:
                raise RuntimeError('Falha ao inserir documento: ID não retornado')
            
            return doc_id

        except RuntimeError:
            raise
        except Error as e:
            raise RuntimeError('Erro ao executar INSERT em documents') from e