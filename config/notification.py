import os
from dotenv import load_dotenv

# Load environment variables (from .env) and add them to the os.getenv() function
load_dotenv()

NOTIFICATIONS = {
    "driver": os.getenv('NOTIFICATION_DRIVER'),
    "always": os.getenv('NOTIFICATION_ALWAYS'),  # Always send notifications

    "onesignal": {
        "app_id": os.getenv('ONESIGNAL_APP_ID'),
        "rest_api_key": os.getenv('ONESIGNAL_REST_API_KEY'),
        "user_auth_key": os.getenv('ONESIGNAL_USER_AUTH_KEY'),
    },
}
