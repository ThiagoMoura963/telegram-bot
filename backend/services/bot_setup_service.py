import requests

class BotSetupService:
    def __init__(self):
        self.api_base_url = 'https://api.telegram.org/bot'

    def register_webhook(self, token: str, webhook_url: str):
        endpoint = f'{self.api_base_url}{token}/setWebhook'
        try:
            response = requests.post(
                endpoint,
                data={'url': webhook_url},
                timeout=10
            )

            result = response.json()

            if result.get('ok'):
                print('[SETUP] Webhook configurada com sucesso.')
                return True, result.get('description', 'Webhook configured') 
            else:
                error_message = result.get('description', 'Unknown error from Telegram API.')
                print(f'[SETUP] Falha ao configurar o Webhook: {error_message}')
                return False, error_message
        except Exception as e:
            error_details = f'Connection error: {str(e)}'
            print(f'[SETUP] Erro crítico: {error_details}')
            return False, error_details 
        
    def get_telegram_info(self, token: str):
        endpoint = f'{self.api_base_url}{token}/getWebhookInfo'
        response = requests.get(endpoint)
        return response.json()
    
    def delete_webook(self, token: str):
        endpoint = f'{self.api_base_url}{token}/deleteWebhook'

        try:
            response = requests.post(endpoint, timeout=10)
            result = response.json()

            if result.get('ok'):
                print('[DELETE] Webhook deletado com sucesso.')
                return True, result.get('description', 'Webhook deleted.')
            else:
                error_message = result('description', 'Failed to delete webhook.')
                print(f'[DELETE] Erro crítico: {error_message}')
                return False, error_message
        except Exception as e:
            error_details = f'Connection error: {str(e)}'
            print(f'[DELETE] Erro crítico: {error_details}')
            return False, error_details 