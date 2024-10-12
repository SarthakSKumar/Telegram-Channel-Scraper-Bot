import asyncio
import os
import time
from telethon import TelegramClient, events
from dotenv import load_dotenv

from clients import Clients
from helpers import Helpers

load_dotenv()

SOURCE_CHANNEL_1 = os.getenv('SOURCE_CHANNEL_1')
SOURCE_CHANNEL_2 = os.getenv('SOURCE_CHANNEL_2')
TARGET_CHANNEL = os.getenv('TARGET_CHANNEL')
UTM = os.getenv('UTM')

BOT_TOKEN = os.getenv('BOT_TOKEN')

Clients = Clients()
Helpers = Helpers()

ListenerClient = Clients.TelegramListenerClient()
BotClient = Clients.TelegramBotClient()

broadcasted_message_ids = {}


async def send_message_to_channel(message_content):
    try:
        await BotClient.send_message(TARGET_CHANNEL, message_content, link_preview=False)
        print(f"Message broadcasted to {TARGET_CHANNEL}")
    except Exception as e:
        print(f"Error broadcasting message: {e}")


def broadcast_message(message):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(send_message_to_channel(message))
    else:
        loop.run_until_complete(send_message_to_channel(message))


async def main():
    await ListenerClient.start()
    await BotClient.start(bot_token=BOT_TOKEN)

    @ListenerClient.on(events.NewMessage(chats=[SOURCE_CHANNEL_1, SOURCE_CHANNEL_2]))
    async def handler(event):
        print("")
        Helpers.cleanup_expired_ids(broadcasted_message_ids)

        if event.message.message and event.message.id not in broadcasted_message_ids:
            message_content = event.message.message
            print("message", message_content, f"{'-'*10}")
            if (Helpers.validate_message_content(message_content)):
                message_content = Helpers.modify_urls(
                    message_content, UTM)

                print("modified message", message_content)

                formatted_message = f"{message_content}\n"
                broadcast_message(formatted_message)

                print("message broadcasted")

                broadcasted_message_ids[event.message.id] = time.time()

    print("Listening for messages...")
    await ListenerClient.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
