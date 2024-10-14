import os
from helpers import Helpers  # Assuming the class is in a file named helpers.py

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the Helpers class
helpers = Helpers()

# Sample message to process
message = """
🔥🔥

Acer 32 inches HD LED TV at 7999.

amazon.in/dp/B0C4YCSF2R?tag=anilfacts0e-21

Redmi (32 inches) Smart LED Fire TV at 10,349

https://www.amazon.in/dp/B0D4LJ9WVW?tag=anilfacts0e-21

Rs.1149 Off With BOB/HSBC/INDUSIND."""

# Step 1: Validate the message content
if helpers.validate_message_content(message):
    # Step 2: Modify the message
    modified_message = helpers.modify_message(message)

    # Step 3: Modify the URLs
    # Get UTM parameter from environment variables
    utm_param = os.getenv('UTM')
    modified_message_with_urls = helpers.modify_urls(
        modified_message, utm_param)

    # Print the final processed message
    print("Processed Message:")
    print(modified_message_with_urls)
else:
    print("Message is invalid or contains invalid URLs.")
