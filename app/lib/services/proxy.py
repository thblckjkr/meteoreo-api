# Checks if the proxy server is running. The file is stored in /mnt/proxy
service = {
  "command": "test -f /mnt/proxy/proxy.pid && kill -0 $(cat /mnt/proxy/proxy.pid)",
  "description": "Check if the proxy server is running",
  "solution": "If the proxy server is not running, run the following command: sudo /mnt/proxy/proxy.py",
  "path": "proxy.actions.check_if_running"
}

service = {
    "command": "echo $(awk '/root/{print $4}' /proc/mounts | awk -F , '{print $1}')",
    "stdout": "ro",
    "stderr": None,
    "actions": {
        "read_write_enabled": {
            "description": "La estación está en modo escritura",
            "solution": "Reactivar el modo sólo lectura",
            "response_stdout": "rw",
            "response_stderr": None,

            # Solution and the expected solution result
            "command": "sudo remountro",
            "stdout": None,
            "stderr": None,
        }
    }
}
