from masoniteorm.models import Model
from masoniteorm.scopes import UUIDPrimaryKeyMixin, SoftDeletesMixin
from masoniteorm.relationships import has_many

class StationAdditional(Model, SoftDeletesMixin):
  """StationAdditional Model"""

  __hidden__ = ["created_at", "updated_at", "deleted_at"]
