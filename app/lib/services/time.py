import time

# Checks the time (station time is important, to preserve data consistency

# Get's and compares the datetime against the current time in bash
command = 'TARGET=$(date -d {0} +%s); CURRENT=$(date +%s); MINUTES=$(( ($TARGET - $CURRENT) / 60 ));'.format(int(time.time()))

# Checks if the obtained minutes is greater than 15 minutes, prints true if it is.
command += 'if [ $MINUTES -gt 15 ]; then echo "true $MINUTES"; else echo "false"; fi'

service = {
    "command": command,
    "stdout": "false",
    "stderr": None,

    "actions": {
        "bad_time": {
            "description": "Por alguna extraña razón el comando date '+%\s' dió error",
            "solution": "Por favor, revisa el comando date en la estación",
            "response_stderr": "",
            "response_stdout": "",
            "action": "No hay nada que hacer"
        }
    }
}
