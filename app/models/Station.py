import ipaddress
import uuid

from masoniteorm.models import Model
from masoniteorm.scopes import UUIDPrimaryKeyMixin, SoftDeletesMixin


class Station(Model, UUIDPrimaryKeyMixin, SoftDeletesMixin):
  """Station Model"""
  # Station model configuration
  __uuid_version__ = 4
  __appends__ = [ "ip_address" ]
  __hidden__ = [ "id", "created_at", "updated_at", "deleted_at" ]

  # Gets ip as a ipaddress class
  def get_ip_address_attribute(self):
    return str(ipaddress.ip_address(self.ip))

  def set_ip_attribute(self, attribute):
    return int(ipaddress.ip_address(attribute))
