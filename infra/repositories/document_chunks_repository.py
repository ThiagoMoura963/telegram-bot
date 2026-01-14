import config
from database import PostgresManager
from psycopg2 import Error
from psycopg2.extras import execute_values
from typing import Any

class DocumentChunksRepository:
    def __init__(self) -> None:
        self.db_manager = PostgresManager(
            config.POSTGRES_USERNAME,
            config.POSTGRES_PASSWORD,
            config.POSTGRES_HOST,
            config.POSTGRES_PORT,
            config.POSTGRES_DATABASE,
        )

    def bulk_insert(
        self,
        document_id: int,
        chunks_data: list[tuple[str, list[float], int]],
    ) -> None:
        sql = """
            INSERT INTO app.document_chunks
            (document_id, content, content_vector, sequence_id)
            VALUES %s
        """

        values = [
            (document_id, content, vector, sequence_id)
            for content, vector, sequence_id in chunks_data
        ]

        try:
            with self.db_manager as cur:
                assert cur is not None

                execute_values(cur, sql, values)

        except Error as e:
            raise RuntimeError("Erro ao inserir chunks em lote") from e

    def find_similar_chunks(
        self,
        query_embedding: Any,
        limit: int,
    ) -> list[str]:
        sql = """
            SELECT content
            FROM app.document_chunks
            ORDER BY content_vector <=> %s
            LIMIT %s
        """

        try:
            with self.db_manager as cur:
                assert cur is not None

                cur.execute(sql, (query_embedding, limit))
                rows = cur.fetchall()

                return [row[0] for row in rows]

        except Error as e:
            raise RuntimeError(
                "Erro ao buscar chunks similares"
            ) from e
