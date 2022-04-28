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

# from pydantic import BaseModel
# from fastapi import Query

from ..Executor.ExecutorFactory import ExecutorFactory
from ..Exceptions.Generic import *
import socket
import os
import subprocess
import time
import logging

# Ejecutor por defecto
DRIVER_EXECUTOR = 'SSH'

def get_element(element, array):
  keys = element.split('.')
  rv = array
  for key in keys:
    rv = rv[key]
  return rv


class BaseDriver():

  def __init__(self, station, services_map=None):
    self.logger = logging.getLogger(__name__)

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
    #TODO: Only check for the services that are in the services_map and the station services array
    for service, operations in self.services_map.items():
      status = None
      [ stdout, stderr ] = self.executor.run(operations['command'])

      # Checks if the stdout and stderr matches the operations stdout and stderr.
      # If the operations are None, we check if the stdout and stderr length is 0
      if ((operations['stdout'] is None and stdout == '') or operations['stdout'] in stdout) and \
          ((operations['stderr'] is None and stderr == '') or operations['stderr'] in stderr):
          self.logger.info("The service %s is running correctly" % service)
          self.logger.info("command: %s" % operations['command'])
          self.logger.info("stdout: %s" % stdout)
          self.logger.info("stderr: %s" % stderr)
          continue
          # If the service is OK, we pass
      else:
        # Check in the array of operations actions, and check if the stderr matches one of them
        for name, action in operations['actions'].items():
          if ((action['response_stdout'] is None and stdout == '') or action['response_stdout'] in stdout) and \
              ((action['response_stderr'] is None and stderr == '') or action['response_stderr'] in stderr):
            # If the stderr matches, we add the action to the problems
            status = {
                'service': service,
                'action': name,
                'stdout': stdout,
                'stderr': stderr,
                'description': action['description'] if 'description' in action else 'No hay descripción',
                'solution': action['solution'] if 'solution' in action else 'No hay solución',
                'command': action['command'] if 'command' in action else None,
                'path': f'%s.actions.%s' % (service, name)
            }
            break

        # If the stderr does not match any action, we add the service to the problems
        if status is None:
          status = {
              'service': service,
              'stdout': stdout,
              'stderr': stderr,
              'description': None,
              'solution': None,
              'command': None,
              'path': f'%s.actions' % service
          }

        problems.append(status)

    return None if len(problems) == 0 else problems

  def fix(self, path):
    """Fixes a problem on the station

    Args:
        path (str): The path of the problem to be fixed
    """

    # Gets the action to be performed from the path
    main_action = get_element(path, self.services_map)

    # Gets the command to execute
    command = main_action['command']

    # Executes the command
    [stdout, stderr] = self.executor.run(command)

    if ((main_action['stdout'] is None and stdout == '') or main_action['stdout'] in stdout) and \
      ((main_action['stderr'] is None and stderr == '') or main_action['stderr'] in stderr):
      return {
            'status': 'success',
            'stdout': stdout,
            'stderr': stderr
        }

    # Checks for the current stdout on the actions dictionary
    for name, action in main_action['actions'].items():
      if ((action['response_stdout'] is None and stdout == '') or action['response_stdout'] in stdout) and \
        ((action['response_stderr'] is None and stderr == '') or action['response_stderr'] in stderr):
          # If the stderr matches, we add the action to the problems
            return {
              'status': 'error',
              'problem': {
                  'service': service,
                  'action': name,
                  'stdout': stdout,
                  'stderr': stderr,
                  'description': action['description'] if 'description' in action else 'No hay descripción',
                  'solution': action['solution'] if 'solution' in action else 'No hay solución',
                  'command': action['command'] if 'command' in action else None,
                  'path': f'%s.actions.%s' % (service, name)
              }
            }

    # If the stderr does not match any action, we return the raw response
      status = {
        'status': 'error',
        'problem': {
          'service': service,
          'stdout': stdout,
          'stderr': stderr,
          'description': None,
          'solution': None,
          'command': None,
          'path': f'%s.actions' % service
        }
      }

# Todo what if the action do not have actions or a command?
