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
  def __init__(self, action_path, action_name, error_message):
    self.action_path = action_path
    self.action_name = action_name
    self.message = error_message
    super.__init__(self.message)
