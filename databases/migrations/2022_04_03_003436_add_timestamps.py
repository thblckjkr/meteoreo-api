"""AddTimestamps Migration."""

from masoniteorm.migrations import Migration


class AddTimestamps(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("event_solutions") as table:
            table.timestamps()
            pass

    def down(self):
        """
        Revert the migrations.
        """
        pass
