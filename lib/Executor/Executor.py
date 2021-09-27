# Standard imports
from abc import ABCMeta, abstractmethod

class ExecutorBase(metaclass=ABCMeta):
  """ Base class for an executor """

  def __init__(self, **kwargs):
    """ Constructor """
    pass

  @abstractmethod
  def run(self, command: str) -> (str, str):
    """ Abstract method to run a command """
    pass
