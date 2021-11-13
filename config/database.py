import os
import logging

from masoniteorm.connections import ConnectionResolver
from dotenv import load_dotenv

# Load environment variables (from .env) and add them to the os.getenv() function
load_dotenv()

DATABASES = {
    "default": os.getenv("DB_CONN", "mysql"),

    "mysql": {
        "driver": "mysql",
        "host": os.getenv("MYSQL_HOST", "mysql"),
        "port": os.getenv("MYSQL_PORT", "3306"),
        "database":  os.getenv("MYSQL_DATABASE"),
        "user":  os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "logging_queries": True,
    },

    "postgres": {
        "driver": "postgresql",
        "host": os.getenv("POSTGRES_HOST", "postgres"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "database": os.getenv("POSTGRES_DATABASE"),
        "user":  os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
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
