from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class Schema(BaseModel):
  name: str = Query(
      None,
      title="Station name",
      description="User identifiable name for the station, this will be used on the main UI",
      min_length=3,
      max_length=255
  )

  """ Driver for the station
  Must be in format driverModule.driverClass, and present on the lib/drivers folder
  """
  driver: str = Query(
      None,
      title="Station driver",
      description="Driver for the station, must be in format driverModule.driverClass",
      min_length=3,
      max_length=255,
      regex=r'^[a-zA-Z0-9_.]+\.[a-zA-Z0-9_]+$'
  )

  """ IP validated with a regex
  See: https://stackoverflow.com/a/17871737
  """
  ip: str = Query(
      None,
      title="Query string",
      description="Query string for the items to search in the database that have a good match",
      regex=r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
  )

  """ The port of the station, is a integer between 0 and 65535
  """
  port: int = Query(
      None,
      title="Station port",
      description="The port of the station, is a integer between 0 and 65535",
      gt=0,
      lt=65536
  )

  """ An optional username to log to the station
  """
  username: Optional[str] = Query(
      None,
      title="Station username",
      description="An optional username to log to the station",
      min_length=2,
      max_length=255
  )

  """ An optional password to log to the station
  """
  password: Optional[str] = Query(
      None,
      title="Station password",
      description="An optional password to log to the station",
      min_length=3,
      max_length=255
  )

  """ HasKey is a boolean, if the station has the SSH key of the server already
  as an authorized key
  """
  has_key: bool = Query(
      None,
      title="Station has key",
      description="HasKey is a boolean, if the station has the SSH key of the server already as an authorized key"
  )
