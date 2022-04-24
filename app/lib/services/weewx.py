# Check the WeeWX service
service = {
    # Este es el comando que ejecutamos para obtener los datos del servicio
    "command": "systemctl status weewx",
    "stdout": "Active: active (running)",
    "stderr": None,  # None implica que esperamos que se encuentre vacío

    # Y esto es lo que esperamos, en out o err, según sea el caso

    # Directiva de problemas que nos podemos encontrar, junto con sus respectivas acciones y soluciones
    # "weewx.serialError.noConnection.action"
    "actions": {
        "unable_to_wake": {
            "description": "Problema de conexión a la consola Davis por puerto serial",
            "solution": "Reinicia la memoria de la consola Davis por medio de la opción --clear-memory",
            "response_stdout": "vantage: Unable to wake up console",
            "response_stderr": None,
            "command": "sudo wee_device --clear-memory && sudo wee_device --info",
            "actions": {
                # There is no connection to clear the memory of the station
                "bad_serial": {
                        "description": "No tenemos conexión para limpiar la memoria de la estación",
                        "solution": "Restart serial connection",
                        "response_stdout": "OSError: [Errno 11] Resource temporarily unavailable",
                        "response_stderr": None,
                        "command": "sudo systemctl stop serial-getty@ttyS0.service"
                }
            }
        }
    }
}
