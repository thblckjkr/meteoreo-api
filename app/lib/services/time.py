import time

# Checks the time (station time is important)
service = {
    "command": "date '+%s'",
    # Hack to get the time near +- 16 minutes of when the time was asked
    "stdout": str(int(int(time.time()) / 1000)),
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
