"""EventsFix Migration."""

from masoniteorm.migrations import Migration


class EventsFix(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("station_events") as table:
          # Makes the event_solution_id nullable, because it can be null if there is no a solution yet
          table.integer("event_solution_id").change().nullable().unsigned()

          table.add_foreign('event_solution_id.id.event_solutions')


    def down(self):
        """
        Revert the migrations.
        """
        pass
