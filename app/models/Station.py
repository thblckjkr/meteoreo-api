import ipaddress
import uuid

from masoniteorm.models import Model
from masoniteorm.scopes import UUIDPrimaryKeyMixin, SoftDeletesMixin
from masoniteorm.relationships import has_many


class Station(Model, UUIDPrimaryKeyMixin, SoftDeletesMixin):
  """Station Model"""
  # Station model configuration
  __uuid_version__ = 4
  __appends__ = ["ip_address"]
  # __with__ = ["events"]

  __hidden__ = ["created_at", "updated_at", "deleted_at"]

  __casts__ = { "services": "json" }

  # Gets ip as a ipaddress class
  def get_ip_address_attribute(self):
    return str(ipaddress.ip_address(self.ip))

  def set_ip_attribute(self, attribute):
    try:
      ip = ipaddress.ip_address(attribute)
    except ValueError:
      raise ValueError("Invalid IP Address %s" % attribute)

    return int(ipaddress.ip_address(attribute))

  @has_many( "id", "station_id")
  def events(self):
    from app.models.StationEvent import StationEvent
    return StationEvent
