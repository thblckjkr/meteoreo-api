# Class that acts as the main bridge between services and drivers

# stores the information about the services, generates alerts and stores them on the database

import importlib
import logging
from app.models.Station import Station

logger = logging.getLogger(__name__)


class Reporter:
  def __init__(self):
    """Constructor for the reporter

    This method is called when the reporter is created.
    """
    pass

  def routine(self):
    """Runs the routine for the reporter

    This method is called by the scheduler and runs the routine for the reporter.
    """
    stations = self.get_stations()

    print("Running routine for reporter")
    for station in stations:
      print("Checking station: " + station.name)
      self.get_station_status(station)

  def get_stations(self):
    """Get a list of the available stations

    Using the app/models/Station, gets the stations that are available
    """
    return Station.get()

  def get_station_status(self, station):
    """Load the driver and get the status of the station, generates an event if neccessary.

    """
    # Loads the driver from the station.drvier parameter. Assumes that the driver specification is in the form of "module.class"
    module = importlib.import_module(
        "lib.drivers" + "." + station.driver.split(".")[0])
    driver = getattr(module, station.driver.split(".")[1])
    instance = driver(station.ip_address, station.port,
                      station.username, "climasUACJ")

    # Connects to the station, checks the status and generates an event if neccessary
    instance.connect()
    instance.get_services()
    logger.warning('The station %s using the driver %s was working correctly', station.name, station.driver)

