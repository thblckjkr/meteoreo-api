"""Stations Migration."""

from masoniteorm.migrations import Migration


class MigrationForStations(Migration):
  def up(self):
    """
    Run the migrations.
    """
    with self.schema.create("stations") as table:
      table.uuid("id")
      table.string("name").unique()
      table.unsigned("ip")

      # Define primary ID's
      table.primary('id')

      # stations shouldn't be deleted, just disabled
      table.soft_deletes()
      table.timestamps()

  def down(self):
    """
    Revert the migrations.
    """
    self.schema.drop("stations")
