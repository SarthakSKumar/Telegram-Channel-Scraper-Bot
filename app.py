import asyncio
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
CHANNEL_1 = os.getenv('CHANNEL_1')
CHANNEL_2 = os.getenv('CHANNEL_2')

CHANNEL_USERNAMES = [CHANNEL_1, CHANNEL_2]

client = TelegramClient('Sarthak S Kumar', API_ID, API_HASH)

def get_relative_path(file_path):
    base_dir = os.getcwd()
    return os.path.relpath(file_path, base_dir)

async def main():
    await client.start()

    @client.on(events.NewMessage(chats=CHANNEL_USERNAMES))
    async def handler(event):
        message_content = ""
        content_type = ""

        if event.message.media:
            content_type = "Media"

            file_path = await client.download_media(event.message.media)
            if file_path:
                relative_path = get_relative_path(file_path)
                message_content += f"Media downloaded to: ./{relative_path}\n"
            else:
                message_content += "Failed to download media.\n"

        if event.message.message:
            content_type = "Text" if content_type == "" else content_type + " & Text"
            message_content += event.message.message

        formatted_message = f"New {content_type} Message from {event.chat.title or event.chat.username}:\n{message_content}\n{'-'*50}\n"
        print(formatted_message)

        with open('messages.txt', 'a', encoding='utf-8') as f:
            f.write(formatted_message)

    print("Listening for new messages from channels...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
