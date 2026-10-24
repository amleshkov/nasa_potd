import requests

SEND_MESSAGE_URL = 'https://api.telegram.org/bot{token}/sendMessage'


class TelegramBot:

    def __init__(self, api_token, chat_id):
        self.api_token = api_token
        self.chat_id = chat_id

    def send_message(self, message, disable_notification):
        response = requests.post(
            SEND_MESSAGE_URL.format(token=self.api_token),
            data={
                'chat_id': self.chat_id,
                'disable_notification': disable_notification,
                'parse_mode': 'html',
                'text': message,
            },
            timeout=30,
        )
        response.raise_for_status()
