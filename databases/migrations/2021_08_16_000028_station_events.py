"""StationEvents Migration."""

from masoniteorm.migrations import Migration


class StationEvents(Migration):
  def up(self):
    """
    Run the migrations.
    """
    with self.schema.create("station_events") as table:
      table.increments("id")
      table.uuid("station_id")
      table.string(column="type", length=16, nullable=False)
      table.string(column="path", nullable=True)
      table.json(column="data")
      table.string(column="status")

      table.primary("id")

      #! Soft deletes are needed for auditing.
      table.soft_deletes()
      table.timestamps()

      # Relation with the station_id
      table.add_foreign('station_id.id.stations')

  def down(self):
    """
    Revert the migrations.
    """
    self.schema.drop("station_events")
