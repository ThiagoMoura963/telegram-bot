from fastapi import APIRouter, HTTPException, BackgroundTasks, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from backend.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest
from backend.schemas.user import UserCreate, UserResponse
from backend.services.auth_service import AuthService
from backend.services.user_service import UserService
from backend.services.mail_service import MailService

router = APIRouter(prefix='/api/v1/auth', tags=['Authentication'])

auth_service = AuthService()
user_service = UserService()

@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    try:
        user_id = user_service.create_user(user_in)

        return{
            "id": user_id,
            "full_name": user_in.full_name,
            "email": user_in.email
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao cadastrar: e-mail já em uso ou dados inválidos."
        )

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    result = auth_service.login(form_data.username, form_data.password)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result

@router.post('/forgot-password', status_code=status.HTTP_200_OK)
async def forgot_password(data: ForgotPasswordRequest, background_tasks: BackgroundTasks):
    user = user_service.get_user_by_email(data.email)

    if user:
        code = auth_service.generate_recovery_code(data.email)
        background_tasks.add_task(MailService.send_recovery_email, data.email, code)
        print(f"[CONTROLLER DEBUG] Solicitação de reset para: {data.email}")
    
    return{
        "status": "success",
        "message": "Se o e-mail estiver cadastrado, um código de 6 dígitos foi enviado."
    }

@router.post('/reset-password')
async def reset_password(data: ResetPasswordRequest):
    is_valid = auth_service.validate_recovery_code(data.email, data.code)

    if not is_valid:
        print(f"[CONTROLLER DEBUG] Validação FALHOU para: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código inválido ou expirado"
        )

    success = user_service.update_password(data.email, data.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao atualizar a senha."
        )

    return {"status": "success", "message": "Senha atualizada com sucesso!"}