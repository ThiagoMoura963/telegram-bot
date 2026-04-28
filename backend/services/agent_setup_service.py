import re

import requests

from backend.infra.repositories.agent_repository import AgentRepository


class AgentSetupService:
    def __init__(self, agent_repository):
        self.api_base_url = 'https://api.telegram.org/bot'
        self.repository: AgentRepository = agent_repository

    def activate_agent(self, agent_id, token, webhook_url, user_id):
        success, message = self._register_webhook(token, webhook_url)

        if success:
            try:
                self.repository.update(agent_id, {'is_active': True}, user_id)
                return True, message
            except Exception as e:
                self._delete_webhook(token)
                return False, f'Database error: {str(e)}'

        return False, message

    def deactivate_agent(self, agent_id, token, user_id):
        success, message = self._delete_webhook(token)

        if success:
            try:
                self.repository.update(agent_id, {'is_active': False}, user_id)
                return True, message
            except Exception as e:
                return False, f'Database error: {str(e)}'

        return False, message

    def get_webhook_info(self, token):
        endpoint = f'{self.api_base_url}{token}/getWebhookInfo'

        try:
            response = requests.get(endpoint, timeout=10)
            return response.json()
        except Exception:
            return {'ok': False, 'description': 'Could not connect to Telegram'}

    def validate_token(self, token: str):
        token = token.strip()
        if not re.match(r'^[0-9]{8,10}:[a-zA-Z0-9_-]{35,}$', token):
            return False, 'Token inválido.'

        try:
            response = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
            if response.status_code == 200:
                return True, response.json()['result']

            return False, 'Token inválido ou revogado pelo BotFather.'
        except Exception:
            return False, 'Serviço do telegram indisponível.'

    def _register_webhook(self, token, webhook_url):
        endpoint = f'{self.api_base_url}{token}/setWebhook'

        try:
            response = requests.post(endpoint, data={'url': webhook_url}, timeout=10)
            result = response.json()

            if result.get('ok'):
                return True, result.get('description', 'Webhook configured.')

            return False, result.get('description', 'Unknown error from Telegram API.')
        except Exception as e:
            return False, f'Connection error {str(e)}'

    def _delete_webhook(self, token):
        endpoint = f'{self.api_base_url}{token}/deleteWebhook'

        try:
            response = requests.post(endpoint, timeout=10)
            result = response.json()

            if result.get('ok'):
                return True, result.get('description', 'Webhook deleted.')

            return False, result.get('description', 'Failed to delete webhook.')
        except Exception as e:
            return False, f'Connection error: {str(e)}'
