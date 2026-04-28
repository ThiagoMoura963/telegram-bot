from ..database import PostgresManager


class AgentRepository:
    def __init__(self):
        self.postgres_manager = PostgresManager()

    def _row_to_dict(self, row):
        if not row:
            return None

        return {
            'id': str(row[0]),
            'name': row[1],
            'system_prompt': row[2],
            'description': row[3],
            'telegram_token': row[4],
            'api_token': row[5],
            'is_active': row[6],
            'user_id': row[7],
        }

    def get_all(self, user_id):
        sql = 'SELECT id, name, description FROM app.agents WHERE user_id = %s;'

        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, (user_id,))
                rows = cursor.fetchall()

                if not rows:
                    return []

                return [{'id': str(row[0]), 'name': row[1], 'description': row[2]} for row in rows]
        except Exception as e:
            raise RuntimeError(f'Erro ao buscar os agentes: {e}') from e

    def save(self, name, system_prompt, telegram_token, api_token, user_id, description=""):
        sql = (
            'INSERT INTO app.agents '
            '(name, system_prompt, description, telegram_token, api_token, user_id) '
            'VALUES (%s, %s, %s, %s, %s, %s) '
            'RETURNING id, name, system_prompt, description, telegram_token, api_token, is_active, user_id;'
        )

        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, (name, system_prompt, description, telegram_token, api_token, user_id))
                row = cursor.fetchone()
                return self._row_to_dict(row)
        except Exception as e:
            raise RuntimeError(f'Erro ao inserir agente: {e}') from e
    
    def get_by_id(self, agent_id, user_id):
        sql = (
            'SELECT id, name, system_prompt, telegram_token, api_token, is_active, user_id '
            'FROM app.agents '
            'WHERE id = %s AND user_id = %s;'
        )

        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, (agent_id, user_id))
                return self._row_to_dict(cursor.fetchone())

        except Exception as e:
            raise RuntimeError(f'Erro ao buscar agente({agent_id}): {e}') from e

    def get_by_api_token(self, api_token):
        sql = (
            'SELECT id, name, system_prompt, telegram_token, api_token, is_active, user_id '
            'FROM app.agents '
            'WHERE api_token = %s;'
        )

        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, (api_token,))
                return self._row_to_dict(cursor.fetchone())
        except Exception as e:
            raise RuntimeError(f'Erro ao buscar agente({api_token}): {e}') from e

    def update(self, agent_id, agent_data, user_id):
        sql = (
            'UPDATE app.agents SET '
            'name = COALESCE(%s, name), '
            'system_prompt = COALESCE(%s, system_prompt), '
            'is_active = COALESCE(%s, is_active) '
            'WHERE id = %s AND user_id = %s;'
        )

        params = (
            agent_data.get('name'),
            agent_data.get('system_prompt'),
            agent_data.get('is_active'),
            agent_id,
            user_id,
        )

        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            raise RuntimeError(f'Erro ao atualizar agente({agent_id}): {e}') from e

    def delete(self, agent_id, user_id):
        sql = 'DELETE FROM app.agents WHERE id = %s AND user_id = %s;'

        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, (agent_id, user_id))
                return cursor.rowcount > 0
        except Exception as e:
            raise RuntimeError(f'Erro ao deletar agente({agent_id}): {e}') from e
