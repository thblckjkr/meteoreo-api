from masoniteorm.models import Model
from masoniteorm.scopes import scope, SoftDeletesMixin
from masoniteorm.relationships import belongs_to


class EventSolutions(Model):
  """
  EventSolutions model
  This is the model that provides the ability to store multiple solutions for a given event.
  """

  __hidden__ = ['deleted_at']

  __casts__ = {"data": "json"}
  __fillable__ = [
    'station_event_id',
    'comment',
    'solution',
    'solved_by',
    'solved_at',
    'station_id',
  ]

  @belongs_to("station_id", "id")
  def station(self):
    from app.models.Station import Station
    return Station

  @belongs_to("station_event_id", "id")
  def station_event(self):
    from app.models.StationEvent import StationEvent
    return StationEvent
