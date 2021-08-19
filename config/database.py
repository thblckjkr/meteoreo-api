from masoniteorm.connections import ConnectionResolver
from dotenv import load_dotenv
import os

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
      "port": os.getenv("MYSQL_PORT", 3306),
      "prefix": "",
      "logging_queries": False,
      "options": {
         #
      }
  },
  "sqlite": {
      "driver": "sqlite",
      "database": os.getenv("SQLITE_DATABASE"),
      "logging_queries": False,
  }
}

DB = ConnectionResolver().set_connection_details(DATABASES)
