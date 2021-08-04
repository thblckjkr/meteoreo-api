from masoniteorm.connections import ConnectionResolver

DATABASES = {
  "default": "mysql",
  "mysql": {
    "host": "mysql",
    "driver": "mysql",
    "database": "meteoreo",
    "user": "root",
    "password": "root",
    "port": 3306,
    "prefix": "",
    "logging_queries": False,
    "options": {
      #  
    }
  }
}

DB = ConnectionResolver().set_connection_details(DATABASES)