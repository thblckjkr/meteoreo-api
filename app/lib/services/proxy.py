# Checks if the proxy server is running. The file is stored in /mnt/proxy
service = {
  "command": 'pgrep -x -f "sudo python port-forward.py" >/dev/null && echo "Running" || echo "Not running"',
  "description": "Check if the proxy server is running",
  "stdout": "Running",
  "stderr": None,
  "actions": {
        "start_the_proxy": {
            "description": "El proxy no está corriendo",
            "solution": "Iniciar el servicio de proxy",
            "response_stdout": "Not running",
            "response_stderr": None,

            # Solution and the expected solution result
            "command": "cd /mnt/usb/proxy; sudo python port-forward.py &",
            "stdout": None,
            "stderr": None,
        }
    }
}
