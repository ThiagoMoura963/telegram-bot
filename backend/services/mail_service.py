# type: ignore

import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

load_dotenv('.env.development')

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME', 'temp@example.com'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD', 'temp_password'),
    MAIL_FROM=os.getenv('MAIL_FROM', 'temp@example.com'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME', 'Bot Manager'),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

class MailService:
    @staticmethod
    async def send_recovery_email(email_to: str, code: str):
        html = f"""
        <html>
            <body>
                <p>Olá,</p>
                <p>Você solicitou a recuperação de senha para o seu "
                "Telegram Bot Manager.</p>
                <p>Seu código de verificação é: <strong>{code}</strong></p>
                <p>Este código expira em 10 minutos.</p>
            </body>
        </html>
        """

        message = MessageSchema(
            subject='Recuperação de Senha - Bot Manager',
            recipients=[email_to],
            body=html,
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message)
