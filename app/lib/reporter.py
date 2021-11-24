# Class that acts as the main bridge between services and drivers

# stores the information about the services, generates alerts and stores them on the database

import os
import importlib
import logging
import datetime

from app.models.Station import Station
from app.models.StationEvent import StationEvent
from .Exceptions.Generic import NetworkError

logger = logging.getLogger(__name__)


class Bridge:
  """ Acts as a bridge between the databases and the drivers
  """
  def driver_exists(driver):
    """Checks if a driver exists

    Args:
        driver (str): Driver name

    Returns:
        bool: True if the driver exists, False otherwise
    """
    if driver is None:
      return False

    if driver in Bridge.get_drivers():
      return True
    else:
      return False

  def get_drivers():
    """Gets all the drivers available in the drivers folder

    This function puts a strain on the IO of the system, as it scans all the drivers
    to create a list and return it.

    It should be used only on registration of a station rather than on every scan.
    It's cheaper to try to load the driver and throw an exception than running this function

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
          "." + station.driver.split(".")[0], package="app.lib.drivers")
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
      reporter = StationReporter(station)
      reporter.generate_station_status()

  def refresh_stations(self):
    """Refreshes the stations

    This method helps to refresh the list of services available in each station
    (Helpful for when the driver is updated)
    """
    stations = self.get_stations()

    for station in stations:
      # Create a instance of the driver
      driver = Bridge.get_driver_instance(station)

      # Get the available services according to the driver
      station.services = instance.get_services()

      # Tries to save the station in the database
      try:
        station.save()
      except Exception as e:
        logger.error("Error saving station: %s", str(e))
        continue

  def get_stations(self):
    """Get a list of the available stations

    Using the app/models/Station, gets the stations that are available
    """
    return Station.get()


class StationReporter:

  def __init__(self, station):
    """Constructor for the station reporter

      This method handles the generation of reports of the station
      Also keeps in mind the idea of parallelization in the future.
    """
    self.station = station
    try:
      self.driver = Bridge.get_driver_instance(station)
    except Exception as e:
      # This error would only be triggered if the driver is erased or the class is renamed
      # This is not a problem, so we just log it and move on
      logger.error("Error loading driver: %s", str(e))
      self.generate_event("driver_error")

  def generate_station_status(self):
    """Loads the driver and get the status of the station, generates an event if neccessary.

    Connects to the station via driver, checks the status and generates an event if neccessary
    """
    try:
      self.driver.connect()
      problems = self.driver.scan()

    except NetworkError as e:
      logger.warning(
          "There was a connection error to the station %s", self.station.name)
      self.generate_event("network_error")
      return  # If the network is down, we can't get the status, so we just return and end the function

    except Exception as e:
      # Fatal error that isn't a network error
      logger.error(
          "There was an error while getting the status of the station %s: %s", self.station.name, str(e))
      self.generate_event(e)
      return

    self.station.last_scan = datetime.datetime.now()
    self.station.save()

    # Check the contents of status, to see if there were any errors, and send the errors to the generator
    if problems is not None:
      for problem in problems:
        self.generate_event("service_error", problem)

    # Solve events that were not present in the scan.
    self.solve_events(problems)

    logger.warning('The station %s using the driver %s was correctly scanned',
                   self.station.name, self.station.driver)

  def generate_event(self, error, data=None):
    """ Generates an event for the station

    This method is called when the status of the station changes.

    It first checks if the event already exists, if it does, it updates it, if not, it creates a new one.
    If the event is a network error, but the last scan time of the station is less than ALERT_TIME
    it updates the event.
    """
    if data is None:
      data = {
          'path': "",
      }

    logger.warning("Generating event of type %s for station %s", error, self.station.name)

    # Check if there is an event of the same error type and in the same path
    lastEvent = StationEvent.where({
        "type": error,
        "path": data['path'],
        "station_id": self.station.id,
        "status": "pending"
    }).get()

    if lastEvent.is_empty():
      # If there is no event, create a new one
      event = StationEvent()

      event.station_id = self.station.id
      event.type = error
      event.path = data['path']
      event.data = data
      event.status = "pending"
      event.save()
    else:
      # If there is an event, update the last reported time
      lastEvent.first().touch()

  def solve_events(self, problems):
    """Solves the events of the station

    This method is called when the station was scanned and there were no problems.

    If there were no problems, solve all the previous registered events.

    If there were problems, check if the previous event was a driver or network error,
    if it was, and it was solved, solve the event.

    If there were problems and the problems were service errors, solve the events that were not solved.

    #! TODO: This is not implemented yet
    """
    if problems is None:
      events = StationEvent.unresolved().where({
          "station_id": self.station.id
      }).get()
    else:
      events = StationEvent.unresolved().where({
          "station_id": self.station.id,
          "type": "service_error"
      }).get()

    print("Solving events for station " + self.station.name)
    for event in events:
      event.status = "auto_solved"
      event.comment = None
      event.solution = "Solución automática al escanearse la estación"
      event.solved_by = "auto"
      event.solved_at = datetime.datetime.now()
      event.save()
