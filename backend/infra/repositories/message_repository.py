from backend.infra.database import PostgresManager


class MessageRepository:
    def save(
        self,
        telegram_user_id: str,
        agent_id: str,
        role: str,
        content: str,
        vector_message: list[float] | None = None,
    ) -> None:
        with PostgresManager() as cursor:
            cursor.execute(
                """
                INSERT INTO app.messages (agent_id, telegram_user_id, role, content, vector_message)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (agent_id, telegram_user_id, role, content, vector_message),
            )

    def get_history(self, telegram_user_id: str, agent_id: str, limit: int = 20) -> list[dict]:
        with PostgresManager() as cursor:
            cursor.execute(
                """
                SELECT role, content
                FROM app.messages
                WHERE agent_id = %s AND telegram_user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (agent_id, telegram_user_id, limit),
            )
            rows = cursor.fetchall()

        rows.reverse()
        return [{'role': row[0], 'content': row[1]} for row in rows]

    def search_semantic_history(self, telegram_user_id, agent_id, query_vector, limit=5):
        sql = (
            'SELECT role, content '
            'FROM app.messages '
            'WHERE agent_id = %s '
            'AND telegram_user_id = %s '
            'AND vector_message IS NOT NULL '
            'ORDER BY vector_message <=> %s::vector '
            'LIMIT %s;'
        )

        with PostgresManager() as cursor:
            cursor.execute(sql, (agent_id, telegram_user_id, query_vector, limit))
            rows = cursor.fetchall()

            return [{'role': row[0], 'content': row[1]} for row in rows]

    def delete_history(self, telegram_user_id: str, agent_id: str) -> None:
        with PostgresManager() as cursor:
            cursor.execute(
                """
                DELETE FROM app.messages
                WHERE agent_id = %s AND telegram_user_id = %s
                """,
                (agent_id, telegram_user_id),
            )
