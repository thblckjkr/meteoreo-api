from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class Schema(BaseModel):
  """Base schema for data required to solve an error of a station

  Attributes:
    comment
    solution
    solved_by
  """

  comment: str = Query(
    None,
    description="Additional comments for the solution of the incident",
    max_length=255,
  )

  solution: str = Query(
    None,
    description="Solution of the incident",
    max_length=255,
  )

  solved_by: str = Query(
    None,
    description="User who solved the incident",
    max_length=16,
  )
