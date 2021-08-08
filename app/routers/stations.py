from fastapi import Depends, APIRouter

from ..models import Station
from ..requests import StationRequest

router = APIRouter(
    prefix="/stations",
    tags=["Stations"],
    dependencies=[Depends(StationRequest.Schema), Depends(Station.Station)]
)


@router.get("/")
def read_stations():
  """Get all stations

  Returns:
     Station: Gets all the stations available in the system
  """
  stations = Station.Station.all()
  return {"stations": stations}


@router.put("/")
def put_station(station: StationRequest.Schema):
  """
  Create a station with all the information:
  """
  result = Station.Station.create(
      {
          'name': station.name,
          'ip': station.ip
      }
  )
  return {"result": result}


@router.get("/{station_uuid}")
def read_item(station_uuid: str = None):

  return {"returns": station_uuid}
