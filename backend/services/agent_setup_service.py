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
                self.repository.update(agent_id, { 'is_active': True }, user_id)
                return True, message
            except Exception as e:
                self._delete_webhook(token)
                return False, f'Database error: {str(e)}'
        
        return False, message
        
    def deactivate_agent(self, agent_id, token, user_id):
        success, message = self._delete_webhook(token)

        if success:
            try:
                self.repository.update(agent_id, { 'is_active': False }, user_id)
                return True, message
            except Exception as e:
                return False, f'Database error: {str(e)}'
            
        return False, message
    
    def get_webhook_info(self, token):
        endpoint = f'{self.api_base_url}{token}/getWebhookInfo'
        
        try:
            response = requests.get(endpoint, timeout=10)
            return response.json()
        except Exception as e:
            return {'ok': False, 'description': 'Could not connect to Telegram'}

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
        

    # def register_webhook(self, token: str, webhook_url: str):
    #     endpoint = f'{self.api_base_url}{token}/setWebhook'
    #     try:
    #         response = requests.post(endpoint, data={'url': webhook_url}, timeout=10)

    #         result = response.json()

    #         if result.get('ok'):
    #             print('[SETUP] Webhook configurada com sucesso.')
    #             return True, result.get('description', 'Webhook configured')
    #         else:
    #             error_message = result.get(
    #                 'description', 'Unknown error from Telegram API.'
    #             )
    #             print(f'[SETUP] Falha ao configurar o Webhook: {error_message}')
    #             return False, error_message
    #     except Exception as e:
    #         error_details = f'Connection error: {str(e)}'
    #         print(f'[SETUP] Erro crítico: {error_details}')
    #         return False, error_details

    # def get_telegram_info(self, token: str):
    #     endpoint = f'{self.api_base_url}{token}/getWebhookInfo'
    #     response = requests.get(endpoint)
    #     return response.json()

    # def delete_webook(self, token: str):
    #     endpoint = f'{self.api_base_url}{token}/deleteWebhook'

    #     try:
    #         response = requests.post(endpoint, timeout=10)
    #         result = response.json()

    #         if result.get('ok'):
    #             print('[DELETE] Webhook deletado com sucesso.')
    #             return True, result.get('description', 'Webhook deleted.')
    #         else:
    #             error_message = result('description', 'Failed to delete webhook.')
    #             print(f'[DELETE] Erro crítico: {error_message}')
    #             return False, error_message
    #     except Exception as e:
    #         error_details = f'Connection error: {str(e)}'
    #         print(f'[DELETE] Erro crítico: {error_details}')
    #         return False, error_details
