import asyncio
import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
CHANNEL_1 = os.getenv('CHANNEL_1')
CHANNEL_2 = os.getenv('CHANNEL_2')
TARGET_CHANNEL = 'the_post_project'

CHANNEL_USERNAMES = [CHANNEL_1, CHANNEL_2]

client = TelegramClient('listener_session', api_id=API_ID, api_hash=API_HASH)

bot = TelegramClient('broadcast_bot', api_id=API_ID, api_hash=API_HASH)

broadcasted_message_ids = set()


async def send_message_to_channel(message_content):
    try:
        await bot.send_message(TARGET_CHANNEL, message_content)
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
    await client.start()
    await bot.start()

    @client.on(events.NewMessage(chats=CHANNEL_USERNAMES))
    async def handler(event):
        if event.message.message and event.message.id not in broadcasted_message_ids:
            message_content = event.message.message
            formatted_message = f"New Message from {event.chat.title or event.chat.username}:\n{message_content}\n{'-' * 50}\n"
            broadcast_message(formatted_message)
            broadcasted_message_ids.add(event.message.id)

    print("Listening for new messages from channels...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
