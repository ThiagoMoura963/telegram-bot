import secrets

from backend.core.security import Security
from backend.infra.redis import redis_manager
from backend.services.user_service import UserService


class AuthService:
    def __init__(self):
        self.redis = redis_manager.client
        self.code_expiry = 600
        self.user_service = UserService()

    def login(self, email: str, password: str):
        user_id = self.user_service.authenticate_user(email, password)

        if not user_id:
            return None

        access_token = Security.create_access_token(data={'sub': str(user_id)})

        return {'access_token': access_token, 'token_type': 'bearer'}

    def generate_recovery_code(self, email: str) -> str:
        code = ''.join(secrets.choice('0123456789') for _ in range(6))
        key = f'password_reset:{email}'
        self.redis.set(key, code, ex=self.code_expiry)

        print(f'\n[REDIS DEBUG] Código gerado para {email}: {code} (Expira em 10min)\n')

        return code

    def validate_recovery_code(self, email: str, user_code: str, auto_delete: bool = True) -> bool:
        key = f'password_reset:{email}'
        stored_code = self.redis.get(key)

        if not stored_code:
            return False

        if isinstance(stored_code, bytes):
            stored_code = stored_code.decode('utf-8')

        if stored_code == user_code:
            if auto_delete:
                self.redis.delete(key)
            return True

        return False
