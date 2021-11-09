from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin


class StationEvent(Model, SoftDeletesMixin):
  """
  StationEvent model
  This is the model to store the events from the stations, such as
  when the station goes offline or has a problem, etc.
  """

  __hidden__ = ['deleted_at']

  __casts__ = { "data": "json" }
