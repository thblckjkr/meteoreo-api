"""Stations Migration."""

from masoniteorm.migrations import Migration

class MigrationForStations(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("stations") as table:
            table.increments("id")
            table.string("name")
            table.unsigned("ip")
            table.uuid("uuid")
            # table. Reference to type

            # stations shouldn't be deleted, just disabled
            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("stations")
