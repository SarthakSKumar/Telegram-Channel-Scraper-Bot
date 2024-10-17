import asyncio
import os
import time
import logging
from telethon import TelegramClient, events
from dotenv import load_dotenv

from clients import Clients
from helpers import Helpers

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SOURCE_CHANNELS = os.getenv('SOURCE_CHANNELS').split(',')
TARGET_CHANNEL = int(os.getenv('TARGET_CHANNEL'))

UTM = os.getenv('UTM')
BOT_TOKEN = os.getenv('BOT_TOKEN')

clients = Clients()
helpers = Helpers()

listener_client = clients.TelegramListenerClient()
bot_client = clients.TelegramBotClient()

broadcasted_message_ids = {}


async def send_message_to_channel(message_content):
    try:
        await bot_client.send_message(TARGET_CHANNEL, message_content, link_preview=False, parse_mode='markdown')
        logger.info(
            f"Sent 📩")
    except Exception as e:
        logger.error(f"Error broadcasting message: {e}")


def broadcast_message(message):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(send_message_to_channel(message))
    else:
        loop.run_until_complete(send_message_to_channel(message))


async def process_message(event):
    helpers.cleanup_expired_ids(broadcasted_message_ids)

    if event.message.message and event.message.id not in broadcasted_message_ids:
        message_content = event.message.message
        logger.info(
            f"New Message: {event.message.peer_id}")

        if helpers.validate_message_content(message_content):
            logger.info("Valid ✅")
            message_content = helpers.modify_message(message_content)
            message_content = helpers.modify_urls(message_content, UTM)
            logger.info(
                f"Modified ✅")

            formatted_message = f"{message_content}\n"

            broadcast_message(formatted_message)

            broadcasted_message_ids[event.message.id] = time.time()
        else:
            logger.warning("Invalid ❌")


async def main():
    await listener_client.start()
    await bot_client.start(bot_token=BOT_TOKEN)

    @listener_client.on(events.NewMessage(chats=list(SOURCE_CHANNELS)))
    async def handler(event):
        asyncio.create_task(process_message(event))

    logger.info("Listening for messages...")
    await listener_client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
