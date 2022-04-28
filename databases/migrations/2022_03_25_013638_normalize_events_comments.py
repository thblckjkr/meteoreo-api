"""NormalizeEventsComments Migration."""

from masoniteorm.migrations import Migration


class NormalizeEventsComments(Migration):
  def up(self):
    """
    Run the migrations.
    """
    with self.schema.create("event_solutions") as table:
      table.increments("id")
      table.string("comment", nullable=True)
      table.string("solution", nullable=True)
      table.string("solved_by", length=16, nullable=True)
      table.integer("station_event_id").unsigned()
      table.uuid("station_id") # Denormalized, sacrifice performance for simplicity
      table.timestamp("solved_at")

      table.add_foreign('station_id.id.stations')
      table.add_foreign('station_event_id.id.station_events')

    with self.schema.table("station_events") as table:
      table.integer("event_solution_id").unsigned()
    #   table.drop_column("comment")
    #   table.drop_column("solution")
    #   table.drop_column("solved_by")
    #   table.drop_column("solved_at")
    #   pass
    pass

  def down(self):
    """
    Revert the migrations.
    """
    with self.schema.table("station_events") as table:
      table.drop_foreign('station_id.id.stations')
      table.drop_foreign('station_event_id.id.station_events')

      table.string("comment", nullable=True)
      table.string("solution", nullable=True)
      table.string("solved_by", length=16, nullable=True)
      table.timestamp("solved_at")
      pass

    with self.schema.table("event_solutions") as table:
      table.drop_table()
      pass
    pass
