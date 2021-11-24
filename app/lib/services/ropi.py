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
