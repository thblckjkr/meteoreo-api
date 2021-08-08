from masoniteorm.models import Model

import ipaddress

class Station(Model):
	"""Station Model"""

	# Gets ip as a ipaddress class
	def get_ip_attribute(self):
		return ipaddress.ip_address(self.ip)

	# Save ip on database as an integer
	def set_ip_attribute(self):
		return int(ipaddress.ip_address(self.ip))
