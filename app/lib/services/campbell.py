# Checks the campbell station, it's located in a given IP address, and it's
# listening on a given port.
# If it's not listening, there is a network error.
# If it's listening, we need to check via curl if there is response

service = {
  # Get's the date of the last update, and compares it with the current date
  # tableName = un_min
  "comand": "curl -s -o /dev/null \"http://{ip}:{port}??command=NewestRecord&table={tableName}"" | grep \"Record Date\" | cut -d ':' -f 2 | cut -d ' ' -f 2",
  "stdout": "200",


}
