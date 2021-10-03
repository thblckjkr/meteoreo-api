# coding: utf-8
#
# This drivers aims to be a simple way to recolect data of a davis station
# connected to a RaspberryPi, runnning a local MySQL database for the
# long-term storage of information, and WeeeWX as the main data recolector.
#
# This program is intended to be able to run directly on the station, with
# a local executor or via SSH from a remote server.
#
# Everything is intended to be run on a command line.
#
# @author: Teo Gonzalez Calzada [@thblckjkr]

from ..Executor.ExecutorFactory import ExecutorFactory
from ..exceptions.Generic import *
import socket
import os
import subprocess
import time

DRIVER_NAME = 'RPiDavisStatus'
DRIVER_EXECUTOR = 'SSH'
DEFAULT_SERVICES_MAP = {
    # Check the MySQL service
    "mysql": {
        "command": "systemctl status mysql",
        "expects": {
            "stdout": "Active: active (running) since",
            "stderr": None
        }
    },

    # Checks the time (station time is important)
    "time": {
      "command": "date '+%s'",
      "expects": {
        # Hack to get the time near +- 16 minutes of when the time was asked
        "stdout": str( int( int( time.time() ) / 1000 ) ),
        "stderr": None,
        "directive": [
          {
            "name": "Por alguna extraña razón el comando date '+%\s' dió error",
            "stderr": "",
            "action": "No hay nada que hacer"
          }
        ]
      }
    },

    # for i in $(seq 30 50); do nc -v -n -z -w 1 148.210.8.$i 22; done
    ""

    # Check the WeeWX service
    "weewx": {
        # Este es el comando que ejecutamos para obtener los datos del servicio
        "command": "systemctl status weewx",

        # Y esto es lo que esperamos, en out o err, según sea el caso
        "expects": {
            "stdout": "Active: active (running)",
            "stderr": None,  # None implica que esperamos que se encuentre vacío

            # Directiva de problemas que nos podemos encontrar, junto con sus respectivas acciones y soluciones
            "directive": [
                {
                    "name": "Problema de conexión a la consola Davis por puerto serial",
                    "expects": {
                        "stdout": "vantage: Unable to wake up console",
                        "action": "sudo wee_device --clear-memory && sudo wee_device --info",

                        "directive": [
                            # There is no connection to clear the memory of the station
                            {
                                "name": "No tenemos conexión para limpiar la memoria de la estación",
                                "expects": {
                                    "stdout": "OSError: [Errno 11] Resource temporarily unavailable",
                                    "action": "sudo systemctl stop serial-getty@ttyS0.service"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
}


class DavisStation():

  def __init__(self, hostname, port, username, password, services_map=None):
    self.services_map = services_map or DEFAULT_SERVICES_MAP
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password
    self.connect()

  # Connnect to the station via the SSH executor
  def connect(self):
    factory = ExecutorFactory()
    factory.register(DRIVER_EXECUTOR)
    self.executor = factory.create_executor(
        DRIVER_EXECUTOR, hostname=self.hostname, port=self.port, username=self.username, password=self.password)

  def get_status(self):
    """Get status of the station

    Tries to get the status before connecting to the station
    to check if it is available.

    We do not trust in paramiko SSH exceptions because the error is too generic

    Returns:
        bool: True if the station is available
    Raises:
        PortConnectionError: If the port (to do SSH) is not available
    """

    # If the connection driver is not SSH, we can't check the connection status
    if DRIVER_EXECUTOR != 'SSH':
      return True

    # Do a ping to the station
    # Using subprocess.run instead of os.system because it does not output the stdout to the console
    command = ['ping', '-c', '1', self.hostname]
    if subprocess.run(command, stdout=subprocess.PIPE).returncode != 0:
      raise IPConnectionError(
          "The station with the IP %s is not available" % self.hostname)

    # Creates a socket to check if the SSH port is accessible
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((self.hostname, self.port))
    if result == 0:
      sock.close()
      return True
    else:
      raise PortConnectionError(
          "The port %d of the IP %s is not reachable" % (self.port, self.hostname))

    # By default, the station is not available
    return False

  def get_services(self):
    # Gets the status first

    if not self.get_status():
      # Somehow, the station is not available but didn't raise an exception
      return None

    # Runs the services check
    for service, operations in self.services_map.items():
      # TODO: Recursion
      [stdout, stderr] = self.executor.run(operations['command'])

      if (operations['expects']['stdout'] == None and len(stdout) == 0) or operations['expects']['stdout'] in stdout:
        if (operations['expects']['stderr'] == None and len(stderr) == 0) or operations['expects']['stderr'] in stderr:
          pass
      else:
        # TODO: Return a better exception, more useful
        raise Exception("Obtenido %s\n Esperado %s" % (stdout, operations['expects']['stdout']))

    return True

    pass

  def fix_service(self):

    pass
