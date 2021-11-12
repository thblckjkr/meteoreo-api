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

from pydantic import BaseModel
from fastapi import Query

from ..Executor.ExecutorFactory import ExecutorFactory
from ..Exceptions.Generic import *
import socket
import os
import subprocess
import time

# Ejecutor por defecto
DRIVER_EXECUTOR = 'SSH'

# List of available drivers for this module (IMPORtANT)
DRIVERS_LIST = ['RpiDavisStation']

DEFAULT_SERVICES_MAP = {
    # Check the MySQL service
    "mysql": {
        "command": "systemctl status mysql",
        "stdout": "Active: active (running) since",
        "stderr": None
    },

    # Checks the time (station time is important)
    "time": {
        "command": "date '+%s'",
        # Hack to get the time near +- 16 minutes of when the time was asked
        "stdout": str(int(int(time.time()) / 1000)),
        "stderr": None,

        "actions": {
            "bad_time": {
                "name": "Por alguna extraña razón el comando date '+%\s' dió error",
                "response_stderr": "",
                "action": "No hay nada que hacer"
            }
        }
    },

    # Check the WeeWX service
    "weewx": {
        # Este es el comando que ejecutamos para obtener los datos del servicio
        "command": "systemctl status weewx",
        "stdout": "Active: active (running)",
        "stderr": None,  # None implica que esperamos que se encuentre vacío

        # Y esto es lo que esperamos, en out o err, según sea el caso

        # Directiva de problemas que nos podemos encontrar, junto con sus respectivas acciones y soluciones
        # "weewx.serialError.noConnection.action"
        "actions": {
            "unable_to_wake": {
                "description": "Problema de conexión a la consola Davis por puerto serial",
                "solution": "Reinicia la memoria de la consola Davis por medio de la opción --clear-memory",
                "response_stdout": "vantage: Unable to wake up console",
                "command": "sudo wee_device --clear-memory && sudo wee_device --info",
                "actions": {
                    # There is no connection to clear the memory of the station
                    "bad_serial": {
                        "description": "No tenemos conexión para limpiar la memoria de la estación",
                        "solution": "Restart serial connection",
                        "response_stdout": "OSError: [Errno 11] Resource temporarily unavailable",
                        "command": "sudo systemctl stop serial-getty@ttyS0.service"
                    }
                }
            }
        }
    },

    # Check the status of ReadOnly Pi
    "RoPi": {
        "command": "echo $(awk '/root/{print $4}' /proc/mounts | awk -F , '{print $1}')",
        "stdout": "ro",
        "stderr": None,
        "actions": {
            "read_write_enabled": {
                "description": "La estación está en modo escritura",
                "solution": "Reactivar el modo sólo lectura",
                "response_stdout": "rw",
                "response_stderr": None,

                # Solution and the expected solution result
                "command": "sudo remountro",
                "stdout": None,
                "stderr": None,
            }
        }
    },
}


class RpiDavisStation():

  def __init__(self, station, services_map=None):
    self.services_map = services_map or DEFAULT_SERVICES_MAP
    self.hostname = station.ip_address
    self.port = station.port
    self.username = station.username

    # If the station has the password attribute, we store in itself
    if hasattr(station, 'password'):
      self.password = station.password

    if station.has_key:
      self.registered = station.has_key

  # Gets the services available to search in the station
  def get_services(self):
    dictionary = self.services_map.keys()
    return list(dictionary)

  # Connnect to the station via the SSH executor
  def connect(self):
    # # Checks if the station has the key registered, if not, register the key
    # if not self.registered and DRIVER_EXECUTOR == 'SSH':
    #   self.register(self.password)

    factory = ExecutorFactory()
    factory.register(DRIVER_EXECUTOR)
    self.executor = factory.create_executor(
        DRIVER_EXECUTOR, hostname=self.hostname, port=self.port, username=self.username)

  def register(self, data):
    password = data.password
    if DRIVER_EXECUTOR != 'SSH':
      return

    factory = ExecutorFactory()
    factory.register(DRIVER_EXECUTOR)
    self.executor = factory.create_executor(
        DRIVER_EXECUTOR, hostname=self.hostname, port=self.port, username=self.username, password=password)

    # Reads the file /app/private_key.pem.pub and appends the key to the to the authorized_keys

    # Enables writing to the station via remountrw (because the file system is read-only)
    # Check ReadOnlyRoot Pi (https://github.com/glennmckechnie/rorpi-raspberrypi) for more info
    [stdout, stderr] = self.executor.run('sudo remountrw')
    if stderr != '':
      raise Exception("Error enabling read-write mode")

    # Assumes get_status was previously called and the station is available
    # Creates the authorized_keys file
    self.executor.run("mkdir -p ~/.ssh")
    [stdout, stderr] = self.executor.run("touch ~/.ssh/authorized_keys")
    if(stderr != ""):
      raise Exception("Error touching authorized_keys file: %s" % stderr)

    # Reads the file /app/private_key.pem.pub and appends the key to the to the authorized_keys
    with open("/app/private_key.pem.pub", "r") as f:
      key = f.read()
      [stdout, stderr] = self.executor.run(
          "echo '%s' >> ~/.ssh/authorized_keys" % key)
      if(stderr != ""):
        raise Exception("Error adding key to authorized_keys file")

    # Restarts the SSH service
    [stdout, stderr] = self.executor.run("sudo systemctl reload sshd")
    if stderr != "":
      raise Exception("Error reloading SSH daemon")

    [stdout, stderr] = self.executor.run('sudo remountro')
    if stderr != "":
      raise Exception("Error disabling read-only mode")

    # Checks if the station has the key registered, if not, register the key
    self.registered = True

    return True

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

  def scan(self):
    """Scans the station and gets the status of the services available on the station

    Returns:
        dict: A dictionary with the problems, or None if everything is ok
    """

    # Initialize an empty array to store the services problems
    problems = []

    # Gets the status first

    if not self.get_status():
      # Somehow, the station is not available but didn't raise an exception
      raise NetworkError("The station is not available")

    # Runs the services check, we need to just recurse the first level
    # This can be changed to a recursive function.
    for service, operations in self.services_map.items():
      [stdout, stderr] = self.executor.run(operations['command'])

      if (operations['stdout'] == None and len(stdout) == 0) or operations['stdout'] in stdout:
        if (operations['stderr'] == None and len(stderr) == 0) or operations['stderr'] in stderr:
          pass
      else:
        # Checks for the current stdout on the actions dictionary
        for name, action in operations['actions'].items():
          if (action['response_stdout'] == None and len(stdout) == 0) or action['response_stdout'] in stdout:
            if (action['response_stderr'] == None and len(stderr) == 0) or action['response_stderr'] in stderr:
              # If it matches, it means that we have a action to do
              status = {
                  'service': service,
                  'action': name,
                  'stdout': stdout,
                  'stderr': stderr,
                  'description': action['description'],
                  'solution': action['solution'],
                  'command': action['command'] if 'command' in action else None,
                  'path': f'%s.actions.%s' % (service, name)
              }

        problems.append(status)

    return None if len(problems) == 0 else problems
