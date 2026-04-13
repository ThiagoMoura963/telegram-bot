import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from backend.core.security import ALGORITHM

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[ALGORITHM])

        user_id: str = payload.get('sub')

        if user_id is None:
            raise credentials_exception

        return int(user_id)

    except (JWTError, ValueError) as e:
        raise credentials_exception from e
