from fastapi import Depends, APIRouter

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
  stations = Station.all( )

  return {
    "stations": stations.serialize()
  }

# -------------------------
# Single station operations
# -------------------------


@router.put("/")
def put_station(stationRequest: StationRequest.Schema):
  """
  Create a station with all the information provided from the StationRequest.Schema
  """
  # TODO: Generate a XML according to the Schema http://cecatev.uacj.mx/Estaciones.xml after the request
  station = Station()

  station.name = stationRequest.name
  station.ip = stationRequest.ip_address
  station.port = stationRequest.port
  station.username = stationRequest.username

  # Create a instance of the driver
  # TODO: Store and use a different services map for each station
  instance = Bridge.get_driver_instance(stationRequest)

  # Get the available services according to the driver
  station.services = instance.get_services()

  # Use the instance of the driver to register the station
  instance.register(stationRequest)


  return station.serialize()


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
  result = Station.get(uuid=uuid).serialize()
  return result


@router.post("/{uuid}")
def post_station(uuid: str, station: StationRequest.Schema):
  """
  Updates a specific station with the information provided from the StationRequest.Schema
  Actualiza una estación específica a los datos que son proveidos en el esquema
  """
  station = Station.get(uuid=uuid)
  station.update(**station.dict())
  return station.serialize()
