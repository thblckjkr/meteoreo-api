from masoniteorm.models import Model
from masoniteorm.scopes import scope, SoftDeletesMixin
from masoniteorm.relationships import belongs_to, has_many


class StationEvent(Model, SoftDeletesMixin):
  """
  StationEvent model
  This is the model to store the events from the stations, such as
  when the station goes offline or has a problem, etc.
  """

  __hidden__ = ['deleted_at']

  __casts__ = {"data": "json"}

  @belongs_to("station_id", "id")
  def station(self):
    from app.models.Station import Station
    return Station

  @has_many("id", "station_event_id")
  def solutions(self):
    from app.models.EventSolutions import EventSolutions
    return EventSolutions

  @scope
  def unresolved(self, query):
    return self.where_not_in('status', [ 'resolved', 'auto_solved', 'ignored' ])

  @scope
  def solvable(self, query):
    return self.type == 'service_error'
