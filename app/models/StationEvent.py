from masoniteorm.models import Model
from masoniteorm.scopes import scope, SoftDeletesMixin
from masoniteorm.relationships import belongs_to


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

  @scope
  def unresolved(self, query):
    return self.where_not_in('status', [ 'resolved', 'auto_solved', 'ignored' ])
