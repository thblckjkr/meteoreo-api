from typing import Callable

import logging
import subprocess
import shlex
import paramiko

from .Executor import ExecutorBase

logger = logging.getLogger(__name__)


class ExecutorFactory:
  """ The factory class for creating executors"""

  registry = {}
  """ Internal registry for available executors """

  @classmethod
  def register(cls, name: str) -> Callable:
    """ Class method to register Executor class to the internal registry.
    Args:
        name (str): The name of the executor.
    Returns:
        The Executor class itself.
    """

    def inner_wrapper(wrapped_class: ExecutorBase) -> Callable:
      if name in cls.registry:
        logger.warning('Executor %s already exists. Will replace it', name)
      cls.registry[name] = wrapped_class
      return wrapped_class

    return inner_wrapper

  # end register()

  @classmethod
  def create_executor(cls, name: str, **kwargs) -> 'ExecutorBase':
    """ Factory command to create the executor.
    This method gets the appropriate Executor class from the registry
    and creates an instance of it, while passing in the parameters
    given in ``kwargs``.
    Args:
        name (str): The name of the executor to create.
    Returns:
        An instance of the executor that is created.
    """

    if name not in cls.registry:
      logger.warning('Executor %s does not exist in the registry', name)
      return None

    exec_class = cls.registry[name]
    executor = exec_class(**kwargs)
    return executor


@ExecutorFactory.register('SSH')
class RemoteExecutor(ExecutorBase):
  def __init__(self, **kwargs):
    """ Constructor """
    self._hostname = kwargs.get('hostname', 'localhost')
    self._port = kwargs.get('port', 22)
    self._username = kwargs.get('username', None)
    self._password = kwargs.get('password', None)
    self._pem = kwargs.get('pem', None)

  def run(self, command: str) -> (str, str):
    """ Runs the command using paramiko """

    # Creates the client, connects and executes the command
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=self._hostname,
                   port=self._port,
                   username=self._username,
                   password=self._password,
                   pkey=paramiko.RSAKey.from_private_key_file(self._pem) if self._pem else None)

    stdin, stdout, stderr = client.exec_command(command)
    out=stdout.read().decode().strip()
    err=stderr.read().decode().strip()

    client.close()
    return out, err


@ExecutorFactory.register('local')
class LocalExecutor(ExecutorBase):

  def run(self, command: str) -> (str, str):
    """ Runs the given command using subprocess """

    args = shlex.split(command)
    stdout, stderr = subprocess.Popen(args,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).communicate()

    out = stdout.decode('utf-8')
    err = stderr.decode('utf-8')
    return out, err
