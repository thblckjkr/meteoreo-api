from fastapi import Depends, APIRouter

from ..models.Station import Station
from ..requests import StationRequest

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
  station = Station().create( stationRequest )

  # station.name = stationRequest.name
  # station.ip = stationRequest.ip
  station.save().fresh()

  return station.serialize()


@router.delete("/{uuid}")
def delete_station(uuid: str):
  """
  Delete a station based on the station uuid
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
