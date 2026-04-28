# type: ignore
import os
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


class OAuth2PasswordBearerCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        header_auth = request.headers.get('Authorization')
        if header_auth and header_auth.startswith('Bearer '):
            return header_auth.replace('Bearer ', '')

        return request.cookies.get('access_token')


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl='/api/v1/auth/login')


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    print('DEBUG - Token capturado:', token[:15] if token else 'Nenhum')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        user_id: str = payload.get('sub')
        if user_id is None:
            raise credentials_exception
        return user_id
    except (JWTError, ValueError) as e:
        raise credentials_exception from e
