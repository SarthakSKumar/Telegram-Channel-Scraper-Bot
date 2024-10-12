from urllib.parse import urlparse, urlunparse


def add_query_to_amazon_urls(message, query_param):
    def modify_amazon_url(url):
        parsed_url = urlparse(url)
        if parsed_url.netloc.endswith('amazon.com') or 'amazon.' in parsed_url.netloc:
            if '/dp/' in parsed_url.path or '/gp/product/' in parsed_url.path:
                return urlunparse((
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path,
                    '',
                    query_param,
                    ''
                ))
        return url

    lines = message.split('\n')
    modified_lines = []

    for line in lines:
        words = line.split()
        modified_words = [modify_amazon_url(word) if word.startswith(
            ('http://', 'https://')) else word for word in words]
        modified_lines.append(' '.join(modified_words))

    return '\n'.join(modified_lines)


# Example usage
test_message = '''Grab FAAASSSTTTT 💥 

Coocaa 43 Inches Full HD Smart LED TV at 10791 (Effectively).
🔗Buy here: https://www.amazon.in/dp/B0BTJ3N57B?psc=1&language=en_IN&tag=anilfacts0e-21

Coocaa 43 Inches Full HD Smart LED TV at 10791 (Effectively).

🔗Buy here: https://www.amazon.in/dp/B0BTJ3N57B?psc=1&language=en_IN&tag=anilfacts0e-21
Coocaa 43 Inches Full HD Smart LED TV at 10791 (Effectively).

🔗Buy here: https://www.amazon.in/dp/B0BTJ3N57B?psc=1&language=en_IN&tag=anilfacts0e-21

Coocaa 43 Inches Full HD Smart LED TV at 10791 (Effectively).:

🔗Buy here: https://www.amazon.in/dp/B0BTJ3N57B?psc=1&language=en_IN&tag=anilfacts0e-21
🔗Buy here: https://www.amazon.in/dp/B0BTJ3N57B?psc=1&language=en_IN&tag=anilfacts0e-21
Coocaa 43 Inches Full HD Smart LED TV at 10791 (Effectively).


₹1699 Discount Using Axis/RBL/Yes Bank CC.'''

modified_message = add_query_to_amazon_urls(test_message, "ref=hello_there")
print(modified_message)
