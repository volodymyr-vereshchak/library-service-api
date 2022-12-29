import telegram
from django.conf import settings


class TelegramBot:
    def __init__(self) -> None:
        self.bot = telegram.Bot(settings.TOKEN)
        
    def send_message(self, message):
        self.bot.send_message(text=message, chat_id="@library_mate")