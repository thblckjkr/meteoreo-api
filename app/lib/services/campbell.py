# Checks the campbell station, it's located in a given IP address, and it's
# listening on a given port.
# If it's not listening, there is a network error.
# If it's listening, we need to check via curl if there is response

class Service:
  def __init__(self, ip, port, tableName):
    if ip is None or port is None or tableName is None:
      raise Exception("ip, port and tableName are required")

    self.ip = ip
    self.port = port
    self.tableName = tableName

  def service(self):
    # Assigns the TARGET datetime to the variable
    command = 'TARGET_STRING=$('

    # Get's the page from the campbell station
    command += 'curl -s "http://{0}:{1}?command=NewestRecord&table={2}" |'.format(self.ip, self.port, self.tableName)

    # From the output of curl, the line <b>Record Date: </b>2022-04-27 17:15:00.0<br>, obtains via SSH the latest record date
    command += 'grep "Record Date" | grep -oP "(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})"'

    # Closes the TARGET datetime, and assigns the response of the command to the variable
    command += ');'

    # Get's and compares the datetime against the current time in bash
    command += 'TARGET=$(date -d "$TARGET_STRING" +%s); CURRENT=$(date +%s); MINUTES=$(( ($TARGET - $CURRENT) / 60 ));'

    # Checks if the obtained minutes is greater than 15 minutes, prints true if it is.
    command += 'if [ $MINUTES -gt 15 ]; then echo "true"; else echo "false"; fi'

    return  {
      "command":  command,
      "stdout": "false",
      "stderr": None,
      "actions": {}
    }
