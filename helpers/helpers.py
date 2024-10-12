import time
import re
from dotenv import load_dotenv
import os

load_dotenv()


class Helpers:
    def __init__(self):
        self.MESSAGE_EXPIRY_TIME = os.getenv('MESSAGE_EXPIRY_TIME')

    def cleanup_expired_ids(self, message_ids):
        current_time = time.time()
        expired_ids = [msg_id for msg_id, timestamp in message_ids.items(
        ) if current_time - timestamp > self.MESSAGE_EXPIRY_TIME]

        for msg_id in expired_ids:
            del message_ids[msg_id]

    def validate_message_content(self, message):
        if not message:
            return False

        amazon_link_pattern = re.compile(
            r'https?://(?:www\.)?amazon\.[a-z\.]{2,6}/dp/([A-Z0-9]{10})(\?.*)?'
        )

        links = re.findall(r'https?://[^\s]+', message)

        if not links:
            return False

        for link in links:
            if not amazon_link_pattern.match(link):
                return False

        return True

    def modify_urls(message, utm):
        def modify_url(url):
            parsed_url = urlparse(url)
            if parsed_url.netloc.endswith('amazon.com') or 'amazon.' in parsed_url.netloc:
                if '/dp/' in parsed_url.path or '/gp/product/' in parsed_url.path:
                    return urlunparse((
                        parsed_url.scheme,
                        parsed_url.netloc,
                        parsed_url.path,
                        '',
                        utm,
                        ''
                    ))
            return url

        lines = message.split('\n')
        modified_lines = []

        for line in lines:
            words = line.split()
            modified_words = [modify_url(word) if word.startswith(
                ('http://', 'https://')) else word for word in words]
            modified_lines.append(' '.join(modified_words))

        return '\n'.join(modified_lines)
