from fastapi import Depends, APIRouter
from ..models.StationEvent import StationEvent

router = APIRouter(
    prefix="/incidents",
    tags=["Drivers"],
    # dependencies=[Depends(StationRequest.Schema), Depends(Station)]
)

@router.get("/")
def get_incidents():
  """
  Get's all the incidents of the stations, regardless of the status
  """
  incidents = StationEvent.all()

  for incident in incidents:
    incident.station = incident.station.serialize()

  return incidents.serialize()

