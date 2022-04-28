"""EventSolutions Migration."""

from masoniteorm.migrations import Migration


class EventSolutions(Migration):
  def up(self):
    """
    Run the migrations.
    """
    with self.schema.table("station_events") as table:
      table.string("comment", nullable=True)
      table.string("solution", nullable=True)
      table.string("solved_by", length=16, nullable=True)
      table.timestamp("solved_at", nullable=True)
      pass

  def down(self):
    """
    Revert the migrations.
    """
    with self.schema.table("station_events") as table:
      table.drop_column("comment")
      table.drop_column("solution")
      table.drop_column("solved_by")
      table.drop_column("solved_at")
