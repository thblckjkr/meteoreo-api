from fastapi import Depends, APIRouter
from ..lib.reporter import Bridge

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
    # dependencies=[Depends(StationRequest.Schema), Depends(Station)]
)

@router.get("/")
def get_drivers():
  """
  Get all the drivers available in the system, this is used to present the end user with the drivers available on the frontend
  """
  return Bridge.get_drivers()
