"""StationTableSeeder Seeder."""

from masoniteorm.seeds import Seeder
from app.models.Station import Station


class StationTableSeeder(Seeder):
  def run(self):
    """Run the database seeds."""
    station = Station()
    station.name = "Estación Babícora"
    station.ip = "148.210.8.32"
    station.port = 22
    station.username = "pi"
    station.driver = "davis.RpiDavisStation"
    station.has_key = False
    station.save()

    station = Station()
    station.name = "Estación Rancho Reforma"
    station.ip = "148.210.8.37"
    station.port = 22
    station.username = "pi"
    station.driver = "davis.RpiDavisStation"
    station.has_key = False
    station.save()

    station = Station()
    station.name = "Estación IIT"
    station.ip = "148.210.123.117"
    station.port = 22
    station.username = "pi"
    station.driver = "davis.RpiDavisStation"
    station.has_key = False
    station.save()

    station = Station()
    station.name = "Estación Anapra"
    station.ip = "148.210.8.31"
    station.port = 22
    station.username = "pi"
    station.driver = "davis.RpiDavisStation"
    station.has_key = False
    station.save()

    station = Station()
    station.name = "Estación Campbell"
    station.ip = "148.210.8.33"
    station.port = 22
    station.username = "pi"
    station.driver = "davis.driverNoExiste"
    station.has_key = False
    station.save()

    station = Station()
    station.name = "Estación Campbell 2"
    station.ip = "148.210.8.2"
    station.port = 22
    station.username = "pi"
    station.driver = "campbell.driverNoExiste"
    station.has_key = False
    station.save()
