from pydantic import BaseModel
# from typing import Optional, Set
from fastapi import Query


class Schema(BaseModel):
  name: str = Query(
      None,
      title="Station name",
      description="User identifiable name for the station, this will be used on the main UI",
      min_length=3,
      max_length=20
  )

  """
  IP validated with a regex
  See: https://stackoverflow.com/a/17871737
  """
  ip: str = Query(
      None,
      title="Query string",
      description="Query string for the items to search in the database that have a good match",
      regex=r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
  )
