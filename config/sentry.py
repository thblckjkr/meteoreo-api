import sentry_sdk
from dotenv import load_dotenv
import os

# Load environment variables (from .env) and add them to the os.getenv() function
load_dotenv()

sentry_sdk.init(
    os.getenv('SENTRY_DSN', None),
    environment=os.getenv('ENVIRONMENT', None),
    traces_sample_rate=1.0,
)
