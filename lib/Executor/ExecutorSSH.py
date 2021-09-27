import logging

from .ExecutorFactory import ExecutorFactory
from .Executor import Executor

import paramiko

@ExecutorFactory.register('davis')
class RemoteExecutor(Executor):
  def __init__(self, **kwargs):
    """ Constructor """
    self._hostname = kwargs.get('hostname', 'localhost')
    self._username = kwargs.get('username', None)
    self._password = kwargs.get('password', None)
    self._pem = kwargs.get('pem', None)

  def run(self, command: str) -> (str, str):
    """ Runs the command using paramiko """

    # Creates the client, connects and executes the command
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=self._hostname,
                   username=self._username,
                   password=self._password,
                   pkey=paramiko.RSAKey.from_private_key_file(self._pem) if self._pem else None)

    _, stdout, stderr = client.exec_command(command)
    out = ''.join(stdout.readlines())
    err = ''.join(stderr.readlines())
    client.close()
    return out, err
