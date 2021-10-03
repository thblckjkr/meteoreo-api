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

DRIVER_NAME = 'RPiDavisStatus'
DRIVER_EXECUTOR = 'SSH'
DEFAULT_SERVICES_MAP = {
    'mysql': {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'davis',
        'table': 'davis_status'
    },
    'vpn': {
        'config': '/etc/openvpn/client.conf'
    },
    'weewx': {

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
    self.executor = factory.create_executor(DRIVER_EXECUTOR, hostname= self.hostname, port = self.port, username = self.username, password = self.password)

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
    if os.system("ping -c 1 " + self.hostname) != 0:
      raise IPConnectionError("The station with the IP %s is not available" % self.hostname)

    # Creates a socket to check if the station is available and running
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((self.hostname, self.port))
    if result == 0:
      sock.close()
      return True
    else:
      raise PortConnectionError("The port %d of the IP %s is not reachable" % (self.port, self.hostname))

    # Check if we can do SSH

    # By default, the station is not available
    return False

    pass

  def get_services(self):
    # Gets the status first
    print (self.get_status())
    # return self.get_status()

    [result, error] = self.executor.run('systemctl status weewx')


    # if result.find("vantage: Unable to wake up console"):
    #   self.executor.run('sudo wee_device --clear-memory')
    #   result = self.executor.run('sudo wee_device --info')
    #   if result.find("OSError: [Errno 11] Resource temporarily unavailable # This line is the important of the output"):
    #     self.executor.run("sudo systemctl stop serial-getty@ttyS0.service")

    print(result)
    pass

  def fix_service(self):

    pass
