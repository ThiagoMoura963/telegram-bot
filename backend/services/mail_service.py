# type: ignore

import os
from dotenv import load_dotenv
from brevo import Brevo
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)
from brevo.core.api_error import ApiError

load_dotenv('.env.development')

client = Brevo(api_key=os.getenv('BREVO_API_KEY', ''))


class MailService:
    @staticmethod
    async def send_recovery_email(email_to: str, code: str):
        html = f"""
        <html>
            <body>
                <p>Olá,</p>
                <p>Você solicitou a recuperação de senha para o seu
                Telegram Bot Manager.</p>
                <p>Seu código de verificação é: <strong>{code}</strong></p>
                <p>Este código expira em 10 minutos.</p>
            </body>
        </html>
        """

        try:
            client.transactional_emails.send_transac_email(
                sender=SendTransacEmailRequestSender(
                    email=os.getenv('MAIL_FROM', 'botmanagerfatec@gmail.com'),
                    name=os.getenv('MAIL_FROM_NAME', 'Bot Manager'),
                ),
                to=[SendTransacEmailRequestToItem(email=email_to)],
                subject='Recuperação de Senha - Bot Manager',
                html_content=html,
            )
        except ApiError as e:
            raise Exception(f'Erro ao enviar email: {e.status_code} - {e.body}')