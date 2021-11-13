"""Stations Migration."""

from masoniteorm.migrations import Migration


class Stations(Migration):
  def up(self):
    """
    Run the migrations.
    """
    with self.schema.create("stations") as table:
      table.uuid("id")
      table.string("name").unique()
      table.unsigned("ip")
      table.unsigned("port")
      table.string("username")
      table.string("driver")
      table.boolean("has_key").default(False)
      table.json(column="services", nullable=True)

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
