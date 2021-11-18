from fastapi import Depends, APIRouter, HTTPException
from ..models.StationEvent import StationEvent
from ..requests import IncidentRequest

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


@router.post("/{id}/solve")
def solve_incident(id: int, incident: IncidentRequest.Schema):
  """
  Solves the incident with the given id

  Note: network_errors and driver_errors should be solved by the reporter automagically
  so, we don't allow them to be solved by the api.

  We have a sepparate method for adding a custom comment to those incidents.
  """
  incident = StationEvent.with_("station").get(id).first()

  if incident is None:
    raise HTTPException(
        status_code=404,
        detail="Incident with id {} not found".format(id)
    )

  if incident.status != "pending":
    raise HTTPException(
        status_code=400,
        detail="Incident with id {} is already solved".format(id)
    )

  if incident.type != "service_error":
    raise HTTPException(
        status_code=400,
        detail="Only service_errors can be solved"
    )

  # Instantiate the driver, sends the path and tries to execute the command to solve it
  instance = Bridge.get_driver_instance(incident.station)

  # Checks the status of the station, according to the driver
  try:
    status = instance.get_status()
  except:
    raise HTTPException(
        status_code=422, detail="Unable to connect to the station")

  # Tries to solve the problem
  try:
    fixed = instance.fix(incident.path)
  except:
    raise HTTPException(
        status_code=422, detail="Unable to connect to the station")

  if fixed == True:
    incident.status = "solved"
    incident.comment = "asdf"
    incident.solution = "Solución automática del problema"
    incident.solved_by = "auto"
    incident.solved_at = datetime.datetime.now()
    incident.save()

  # Tries to solve the incident, loading the driver and executing the path command


