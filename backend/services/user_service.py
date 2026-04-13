from backend.core.security import Security
from backend.infra.database import PostgresManager
from backend.schemas.user import UserCreate


class UserService:
    def create_user(self, user_in: UserCreate):
        hashed_password = Security.get_password_hash(user_in.password)

        query = """
            INSERT INTO app.users (full_name, email, hashed_password, is_active)
            VALUES(%s, %s, %s, %s)
            RETURNING id;
        """

        with PostgresManager() as cursor:
            cursor.execute(query, (user_in.full_name, user_in.email, hashed_password, True))
            user_id = cursor.fetchone()[0]
            return user_id
        
    def authenticate_user(self, email: str, password: str):
        query = "SELECT id, hashed_password FROM app.users WHERE email = %s"

        with PostgresManager() as cursor:
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if not result:
                return None
            
            user_id, hashed_password = result
            if Security.verify_password(password, hashed_password):
                return user_id
            
            return None
        
    def get_user_by_email(self, email):
        query = "SELECT id, full_name FROM app.users WHERE email = %s"
    
        with PostgresManager() as cursor:
            cursor.execute(query, (email,))
            return cursor.fetchone()
    
    def update_password(self, email: str, new_password: str):
        hashed_password = Security.get_password_hash(new_password)

        query = """
            UPDATE app.users 
            SET hashed_password = %s 
            WHERE email = %s
        """

        try:
            with PostgresManager() as cursor:
                cursor.execute(query, (hashed_password, email))
                return True
            
        except Exception as e:
            print(f"[DATABASE ERROR] Erro ao atualizar senha: {e}")
            return False
