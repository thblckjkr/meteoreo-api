from fastapi import Depends, APIRouter, HTTPException

from ..models.Station import Station
from ..requests import StationRequest
from ..lib.reporter import Bridge

from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

router = APIRouter(
    prefix="/stations",
    tags=["Stations"],
    dependencies=[Depends(StationRequest.Schema), Depends(Station)]
)

# --------------------------
# All stations operations
# --------------------------


@router.get("/")
def read_stations():
  """Get all stations

  Returns:
     Station: Gets all the stations available in the system
  """
  stations = Station.all()

  for station in stations:
    station.incidents = station.events.serialize()

  return {
    "stations": stations.serialize()
  }

# -------------------------
# Single station operations
# -------------------------


@router.put("/")
async def put_station(station: StationRequest.Schema):
  """ Creates a station with all the information provided from the Station.Schema

  First, tries to connecto to the station using the credentials provided, then tries to register it,
  and then tries to store it in the database.
  """
  # TODO: Generate a XML according to the Schema http://cecatev.uacj.mx/Estaciones.xml after the request

  # Checks if the driver exists on the drivers from the Bridge
  if not Bridge.driver_exists(station.driver):
    raise HTTPException(status_code=400, detail="Driver not found")

  stationModel = Station()

  stationModel.name = station.name
  stationModel.ip = station.ip
  stationModel.port = station.port
  stationModel.username = station.username
  stationModel.driver = station.driver

  # Create a instance of the driver
  instance = Bridge.get_driver_instance(station)

  # # Get the available services according to the driver
  stationModel.services = instance.get_services()

  # Tries to get the status of the station (if it is online)
  try:
    status = instance.get_status()
  except:
    raise HTTPException(status_code=422, detail="Unable to connect to the station")

  # Use the instance of the driver to register the station
  try:
    instance.register(station)
    stationModel.has_key = True
  except:
    raise HTTPException(status_code=422, detail="Unable to register the station")

  # Store the station in the database
  try:
    stationModel.save()
  except:
    raise HTTPException(status_code=500, detail="Unable to save the station")

  return {
    "status": "Ok",
    "model":stationModel.serialize()
  }

@router.delete("/{uuid}")
def delete_station(uuid: str):
  """
  Delete a station based on the station uuid

  This actually *soft deletes* the station, to preserve the history of the station
  """
  station = Station.get(uuid)
  station.delete()
  return {"message": "station deleted"}


@router.get("/{uuid}")
def get_station(uuid: str):
  """
  Get a specific station from it's uuid
  """
  result = Station.find(uuid)
  result.incidents = result.events.all()

  return result.serialize()


@router.post("/{uuid}")
def post_station(uuid: str, station: StationRequest.Schema):
  """
  Updates a specific station with the information provided from the StationRequest.Schema
  """
  station = Station.get(uuid=uuid)
  station.update(**station.dict())
  return station.serialize()
