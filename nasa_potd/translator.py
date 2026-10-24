import requests

TRANSLATE_API_URL = 'https://translate.api.cloud.yandex.net/translate/v2/translate'


class Translator:

    def __init__(self, api_key):
        self.api_key = api_key

    def translate(self, translate_from, translate_to, texts):
        response = requests.post(
            TRANSLATE_API_URL,
            headers={'Authorization': f'Api-Key {self.api_key}'},
            json={
                'sourceLanguageCode': translate_from,
                'targetLanguageCode': translate_to,
                'texts': texts,
                'speller': True,
            },
            timeout=30,
        )
        response.raise_for_status()
        return [item['text'] for item in response.json()['translations']]
