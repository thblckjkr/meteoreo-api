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
            table.varchar("event_type")
            table.varchar("event_data")

            table.primary("id")
            #! Soft deletes are needed for auditing.
            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("station_events")
