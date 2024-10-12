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

CHANNEL_USERNAMES = [SOURCE_CHANNEL_1, SOURCE_CHANNEL_2]

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
    await BotClient.start()

    @ListenerClient.on(events.NewMessage(chats=CHANNEL_USERNAMES))
    async def handler(event):

        Helpers.cleanup_expired_ids(broadcasted_message_ids)

        if event.message.message and event.message.id not in broadcasted_message_ids:
            message_content = event.message.message
            if (Helpers.validate_message_content(message_content)):
                message_content = Helpers.modify_urls(
                    message_content, UTM)

                formatted_message = f"{message_content}\n"
                broadcast_message(formatted_message)

                broadcasted_message_ids[event.message.id] = time.time()

    print("Listening for messages...")
    await ListenerClient.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
