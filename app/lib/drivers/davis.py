from .base import BaseDriver
from ..services import mysql, ropi, time, weewx, disk

# Ejecutor por defecto
DRIVER_EXECUTOR = 'SSH'

# List of available drivers for this module (IMPORtANT)
DRIVERS_LIST = [ 'RpiDavisStation' ]

DEFAULT_SERVICES_MAP = {
    "mysql": mysql.service,
    "weewx": weewx.service,
    "RoPi": ropi.service,
    "disk": disk.service,
}

class RpiDavisStation(BaseDriver):

  def __init__(self, station, services_map=None):
    services_map = DEFAULT_SERVICES_MAP

    # Refresh time on every instantiation
    services_map['time'] = time.service()

    return super().__init__(station, services_map)
