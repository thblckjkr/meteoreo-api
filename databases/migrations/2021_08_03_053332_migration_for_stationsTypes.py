"""StationTypes Migration."""

from masoniteorm.migrations import Migration


class MigrationForStationTypes(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("station_types") as table:
            table.increments("id")
            table.string("name")

            # Soft deletes to maintain integrity
            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("station_types")
