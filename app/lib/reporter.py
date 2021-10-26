# Class that acts as the main bridge between services and drivers

# stores the information about the services, generates alerts and stores them on the database

import os
import importlib
import logging

from app.models.Station import Station
from .Exceptions.Generic import NetworkError

logger = logging.getLogger(__name__)


class Bridge:
  """ Acts as a bridge between the databases and the drivers
  """
  def get_drivers():
    """Gets all the drivers available in the drivers folder

    Returns:
        list: List of all the drivers
    """
    modules = []
    drivers = []

    for module in os.listdir("app/lib/drivers"):
      if module.endswith(".py"):
        modules.append(module.split(".")[0])

    # Gets the variable DRIVERS_LIST from the driver file and returns it
    # This is a dictionary with the key as the driver name and the value as the driver class
    # e.g. {'mock': <class 'app.lib.drivers.mock.MockDriver'>}
    for module in modules:
      mod = importlib.import_module("app.lib.drivers." + module)
      try:
        drivers_list = getattr(mod, "DRIVERS_LIST")
      except AttributeError:
        logger.error("Module %s has no DRIVERS_LIST", module)
        continue

      available_drivers = [(module + "." + driver) for driver in drivers_list]
      drivers = drivers + available_drivers

    return drivers

  def get_driver_instance(station):
    """Gets the driver of a station and returns it

    Args:
        station ([type]): [description]

    Returns:
        instance: Instance of a driver

    Throws:
        ModuleNotFoundError: If the driver is not found
        AttributeError: If the class driver is not found
    """
    try:
      # Loads the driver from the station.drvier parameter.
      # Assumes that the driver specification is in the form of "module.class"
      module = importlib.import_module(
          "lib.drivers." + station.driver.split(".")[0])
      driver = getattr(module, station.driver.split(".")[1])
      instance = driver(station)
    except ModuleNotFoundError as e:
      logger.error("Error loading driver: %s", str(e))
      raise e
    except AttributeError as e:
      logger.error("Error loading driver, class does not exist: %s", str(e))
      raise e

    return instance



class Reporter:
  def __init__(self):
    """Constructor for the reporter

    This method is called when the reporter is created.
    """

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
    try:
      instance = self.get_driver_instance(station)
    except Exception as e:
      logger.error("Error loading driver: %s", str(e))
      raise e

    # Connects to the station, checks the status and generates an event if neccessary
    try:
      instance.connect()
      status = instance.get_status()
    except NetworkError as e:
      logger.warning(
          "There was a connection error to the station %s", station.name)
      return
    except Exception as e:
      logger.error(
          "There was an error while getting the status of the station %s: %s", station.name, str(e))
      return

    print(status)
    # If the status is different from the last status, generate an event
    # if status != station.last_status:
    #   station.last_status = status
    #   station.save()
    #   self.generate_event(station, status)

    logger.warning('The station %s using the driver %s was working correctly',
                   station.name, station.driver)
