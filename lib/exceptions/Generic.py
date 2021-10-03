# Custom python exception that contains the connection error

# The main idea is to have everything handled by the main exception handler
# and not to have to deal with the connection errors in the code

# Base network error handling
class NetworkError(Exception):
  pass


class PortConnectionError(NetworkError):
  pass


class IPConnectionError(NetworkError):
  pass


class GenericException(Exception):
  action_path = None
  action_name = None
  action_args = None

  def __init__(self, action_path, action_name, action_args):
    self.action_path = action_path
    self.action_name = action_name
    self.action_args = action_args
    Exception.__init__(self)
