# reads the file /var/www/html/Teledyne/actual.html from the server, parses it as an XML and searchs for any field that contains the string "N/A"


import requests
import xml.etree.ElementTree as ET
import time
import datetime
import logging

logger = logging.getLogger(__name__)
