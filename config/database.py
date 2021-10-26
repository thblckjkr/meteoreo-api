import os
import logging

from masoniteorm.connections import ConnectionResolver
from dotenv import load_dotenv

# Load environment variables (from .env) and add them to the os.getenv() function
load_dotenv()

DATABASES = {
    "default": "mysql",
    "mysql": {
        "host": os.getenv("MYSQL_HOST", "mysql"),
        "driver": "mysql",
        "database":  os.getenv("MYSQL_DATABASE"),
        "user":  os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "port": os.getenv("MYSQL_PORT", "3306"),
        # "prefix": "",
        "logging_queries": True,
    },
    "sqlite": {
        "driver": "sqlite",
        "database": os.getenv("SQLITE_DATABASE", "meteoreo.db"),
        "logging_queries": True,
    }
}

logger = logging.getLogger('masoniteorm.connection.queries')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
file_handler = logging.FileHandler('logs/queries.log')

logger.addHandler(handler)
logger.addHandler(file_handler)

DB = ConnectionResolver().set_connection_details(DATABASES)

