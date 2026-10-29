import html
import os
import re

import requests

from . import config

NASA_API_URL = 'https://science.nasa.gov/wp-json/wp/v2/apod-basic'
NASA_API_KEY_DEFAULT = 'DEMO_KEY'


class NasaData:

    def __init__(self):
        response = requests.get(
            NASA_API_URL,
            params={
                'per_page': 1,
                'api_key': os.getenv('NASA_API_KEY', NASA_API_KEY_DEFAULT),
            },
            proxies={'http': config.proxy, 'https': config.proxy} if config.proxy else None,
            timeout=60,
        )
        response.raise_for_status()
        self.apod = response.json()[0]

    def title(self):
        return self.apod['title']

    def explanation(self):
        return self._clean_text(self.apod['explanation'])

    def url(self):
        if self.apod.get('media_type') == 'image':
            return self.apod.get('hdurl').spit('?')[0] or self.apod['url']
        return self.apod['url']

    @staticmethod
    def _clean_text(text):
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.I)
        text = re.sub(r'<[^>]+>', '', text)
        text = html.unescape(text)
        text = re.sub(r'^\s*Explanation:\s*', '', text)
        text = re.sub(r"\n\s*Tomorrow.s picture:.*$", '', text, flags=re.I)
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
