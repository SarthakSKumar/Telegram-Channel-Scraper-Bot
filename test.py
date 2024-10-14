import os
from helpers import Helpers  # Assuming the class is in a file named helpers.py

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the Helpers class
helpers = Helpers()

# Sample message to process
message = """
💥 Jakmister (Anti-Vibration) Unbreakable Plastic 700 W 16000RPM 90 Miles/Hour Electric Air Blower Dust PC Cleaner Forward Curved Air Blower

▶️ Deal @ ₹485/-😱 

Link : https://www.amazon.in/Jakmister-Electric-Blower-Cleaner-16000RPM/dp/B07L4RTJG8?language=en_IN&tag=pavankalyan05-21"""

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
