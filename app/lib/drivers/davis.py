from .base import BaseDriver
from ..services import mysql, ropi, time, weewx

# Ejecutor por defecto
DRIVER_EXECUTOR = 'SSH'

# List of available drivers for this module (IMPORtANT)
DRIVERS_LIST = [ 'RpiDavisStation' ]

DEFAULT_SERVICES_MAP = {
    "mysql": mysql.service,
    "time": time.service,
    "weewx": weewx.service,
    "RoPi": ropi.service,
}

class RpiDavisStation(BaseDriver):

  def __init__(self, station, services_map=None):
    return super().__init__(station, DEFAULT_SERVICES_MAP)
