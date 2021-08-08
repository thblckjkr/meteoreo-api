from masoniteorm.connections import ConnectionResolver
import os

DATABASES = {
  "default": "mysql",
  "mysql": {
    "host": os.getenv("MYSQL_HOST", "mysql"),
    "driver": "mysql",
    "database":  os.getenv("MYSQL_DATABASE"),
    "user":  os.getenv("MYSQL_USERNAME"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "port": os.getenv("MYSQL_PORT", 3306),
    "prefix": "",
    "logging_queries": False,
    "options": {
      #
    }
  }
}

DB = ConnectionResolver().set_connection_details(DATABASES)
