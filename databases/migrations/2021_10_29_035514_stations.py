"""Stations Migration."""

from masoniteorm.migrations import Migration


class Stations(Migration):
  def up(self):
    """
    Run the migrations.
    """
    with self.schema.table("stations") as table:
      table.datetime(column="last_scan", nullable=True)

  def down(self):
    """
    Revert the migrations.
    """
    with self.schema.table("stations") as table:
      table.drop_column("last_scan")
