# type: ignore 

from ..database import PostgresManager

class TelegramUserRepository:
    def __init__(self):
        self.postgres_manager = PostgresManager()
    
    def upsert(self, telegram_id, first_name, username):
        sql = (
            'INSERT INTO app.telegram_users (telegram_id, first_name, username) '
            'VALUES (%s, %s, %s) '
            'ON CONFLICT (telegram_id) '
            'DO UPDATE SET '
            'first_name = EXCLUDED.first_name, '
            'username = EXCLUDED.username '
            'RETURNING id;'
        )
        try:
            with self.postgres_manager as cursor:
                cursor.execute(sql, (telegram_id, first_name, username))
                return str(cursor.fetchone()[0])
        except Exception as e:
            raise RuntimeError(f'Erro ao salvar usuário do Telegram: {e}') from e