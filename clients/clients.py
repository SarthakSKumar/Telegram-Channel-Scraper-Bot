from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

class Clients:
    def __init__(self):
        self.API_ID = os.getenv('API_ID')
        self.API_HASH = os.getenv('API_HASH')

    def TelegramBotClient(self):
        return TelegramClient('bot_client', api_id=self.API_ID, api_hash=self.API_HASH)

    def TelegramListenerClient(self):
        return TelegramClient('listener_client', api_id=self.API_ID, api_hash=self.API_HASH)
