service = {
    "command": "PERCENT=$(df /mnt/usb --output=pcent | tail -n 1 | tr -d '%')" + \
      "if (( $PERCENT > 80 )); then echo \"true $PERCENT\"; else echo \"false $PERCENT\"; fi",
    "stdout": "false",
    "stderr": None,
    "actions": {
        "disk_almost_full": {
            "description": "El disco está casi lleno",
            "solution": "Elimine algunos archivos de la estación",
            "response_stdout": "true",
            "response_stderr": None,
        }
    }
}
