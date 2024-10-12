import time
import re
from dotenv import load_dotenv
import os
import urllib.parse
import urllib.request

load_dotenv()


class Helpers:
    def __init__(self):
        self.MESSAGE_EXPIRY_TIME = float(os.getenv('MESSAGE_EXPIRY_TIME'))

    def cleanup_expired_ids(self, message_ids):
        current_time = time.time()
        expired_ids = [msg_id for msg_id, timestamp in message_ids.items(
        ) if current_time - timestamp > self.MESSAGE_EXPIRY_TIME]

        for msg_id in expired_ids:
            del message_ids[msg_id]

    def validate_message_content(self, message):
        if not message:
            return False

        amazon_url_pattern = re.compile(r'(?<!\s)https://www\.amazon\.in/.*')
        shortened_amazon_url_pattern = re.compile(
            r'(?<!\s)https://amzn\.to/.*')

        links = re.findall(r'https?://[^\s]+', message)

        if not links:
            return False

        for link in links:
            if not (amazon_url_pattern.match(link) or shortened_amazon_url_pattern.match(link)):
                return False

        return True

    def modify_urls(self, message, utm):
        def expand_url(url):
            if 'amzn.to' in url:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                    req = urllib.request.Request(url, headers=headers)

                    with urllib.request.urlopen(req, timeout=10) as response:
                        return response.url
                except Exception as e:
                    return url
            return url

        def modify_url(url):
            expanded_url = expand_url(url)
            parsed_url = urllib.parse.urlparse(expanded_url)

            if parsed_url.netloc.endswith('amazon.com') or 'amazon.' in parsed_url.netloc:
                query_params = urllib.parse.parse_qs(parsed_url.query)

                params_to_remove = ['ds', 'qid', 'tag', 'ref', 'linkCode', 'creative', 'ie', 'ascsubtag',
                                    'adid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'linkId', 'ref_']
                for param in params_to_remove:
                    query_params.pop(param, None)

                new_query = urllib.parse.urlencode(query_params, doseq=True)

                if new_query:
                    new_query += '&' + utm
                else:
                    new_query = utm

                clean_path_segments = [
                    segment for segment in parsed_url.path.split('/')
                    if not any(param in segment for param in params_to_remove)
                ]
                cleaned_path = '/'.join(clean_path_segments)

                modified_url = urllib.parse.urlunparse((
                    parsed_url.scheme,
                    parsed_url.netloc,
                    cleaned_path,
                    '',
                    new_query,
                    ''
                ))
                return modified_url

            return expanded_url

        lines = message.split('\n')
        modified_lines = []

        for line in lines:
            words = line.split()
            modified_words = [modify_url(word) if word.startswith(
                ('http://', 'https://')) else word for word in words]
            modified_lines.append(' '.join(modified_words))

        return '\n'.join(modified_lines)
