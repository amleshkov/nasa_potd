import os

from dotenv import load_dotenv

from . import config
from .message import build_message
from .nasa import NasaData
from .telegram import TelegramBot
from .translator import Translator


def main():
    load_dotenv()
    data = NasaData()
    title = data.title()
    explanation = data.explanation()
    if config.translate:
        translator = Translator(os.getenv('YC_API_TOKEN'))
        title, explanation = translator.translate(
            config.translate_from, config.translate_to, [title, explanation]
        )
    bot = TelegramBot(os.getenv('BOT_TOKEN'), os.getenv('CHAT_ID'))
    bot.send_message(build_message(title, explanation, data.url()), config.disable_notification)


if __name__ == '__main__':
    main()
