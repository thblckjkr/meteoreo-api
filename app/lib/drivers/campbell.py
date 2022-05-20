from .base import BaseDriver
from ..services import mysql, ropi, time, weewx, proxy, campbell, disk

# Ejecutor por defecto
DRIVER_EXECUTOR = 'SSH'

# List of available drivers for this module (IMPORtANT)
DRIVERS_LIST = [ 'RpiCampbellStation' ]

DEFAULT_SERVICES_MAP = {
    "mysql": mysql.service,
    "weewx": weewx.service,
    "RoPi": ropi.service,
    "proxy": proxy.service,
    "disk": disk.service,
}

class RpiCampbellStation(BaseDriver):

  def __init__(self, station, services_map=None):

    services_map = DEFAULT_SERVICES_MAP
    # Get's the extra_data from the station and searches for
    # campbell_ip, #campbell_port y #campbell_table
    extra_data = station.extra_data.serialize()

    # Get's the IP from the extra_data array of dictionaries
    for d in extra_data:
      if d['key'] == 'campbell_ip':
        campbell_ip = d['value']
      if d['key'] == 'campbell_port':
        campbell_port = d['value']
      if d['key'] == 'campbell_table':
        campbell_table = d['value']

    if not campbell_ip:
      raise Exception("No campbell_ip in extra_data")

    if not campbell_port:
      raise Exception("No campbell_port in extra_data")

    if not campbell_table:
      raise Exception("No campbell_table in extra_data")

    # Create the services
    services_map['campbell'] = campbell.Service(
      campbell_ip,
      campbell_port,
      campbell_table
    ).service()

    # Refresh time on every instantiation
    services_map['time'] = time.service()

    return super().__init__(station, services_map)

# Example of the command generated
# TARGET_STRING=$(curl -s "http://192.168.88.2:80?command=NewestRecord&table=un_min" | grep "Record Date" | grep -oP "(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})")
# TARGET=$(date -d "$TARGET_STRING" +%s)
# CURRENT=$(date +%s)
# MINUTES=$((($TARGET - $CURRENT) / 60))
# if [ $MINUTES -gt 15 ]; then echo "true"; else echo "false"; fi
