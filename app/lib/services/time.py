import time

# Checks the time (station time is important, to preserve data consistency
def service():
  # Get's and compares the datetime against the current time in bash
  command = 'CURRENT=$(date +%s); MINUTES=$(( ({0} - $CURRENT) / 60 ));'.format(int(time.time()))

  # Checks if the obtained minutes is greater than 15 minutes, prints true if it is.
  command += 'if (( $MINUTES > 15 || $MINUTES < -15 )); then echo "true $MINUTES"; else echo "false $MINUTES"; fi'

  service = {
      "command": command,
      "stdout": "false",
      "stderr": None,

      "actions": {
          "bad_time": {
            "description": "La fecha es incorrecta",
            "solution": "Verifique la fecha y hora del sistema",
            "response_stdout": "true",
            "response_stderr": None,
            "action": "Ponga la estación a la hora correcta con el comando date -s ",
          },

          "time_error": {
              "description": "Por alguna extraña razón el comando date '+%\s' dió error",
              "solution": "Por favor, revisa el comando date en la estación",
              "response_stderr": "",
              "response_stdout": "",
              "action": "No hay nada que hacer"
          }
      }
  }

  return service
