DRIVER_NAME = 'RPiDavisStatus'

# class DavisStatus(Status):
class DavisStatus():
  DEFAULT_SERVICES_MAP = {
    'mysql': {
      'host': 'localhost',
      'user': 'root',
      'password': '',
      'database': 'davis',
      'table': 'davis_status'
    },
    'vpn':{
      'config': '/etc/openvpn/client.conf'
    }
  }
