"""StationAdditional Migration."""

from masoniteorm.migrations import Migration


class StationAdditional(Migration):
  def up(self):
    """
    Run the migrations.
    """
    with self.schema.create("station_additionals") as table:
      table.increments("id")
      table.string("key")
      table.string("value")
      table.uuid("station_id")

      table.timestamps()
      table.soft_deletes()

      table.add_foreign('station_id.id.stations')

  def down(self):
    """
    Revert the migrations.
    """
    self.schema.drop("station_additionals")
