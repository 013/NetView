#!/usr/bin/env python
from time import sleep
import json

class stats:
	def __init__(self):
		self.JSONfile = './www/stats.json'
		self.history = 2
		
		self.devices = ['eth0']
		self.stats = ['rx_bytes', 'tx_bytes', 'rx_packets', 'tx_packets']
		
		# Create data list
		self.data = list()
		for device in self.devices:
			dev=dict()
			for stat in self.stats:
				dev[stat]=(0,)*self.history
			self.data.append({device:dev})
	
	def getstat(self, inf='rx_packets', dev='eth0'):
		"""
		Compare information 1 second apart
		to see how much was transferred within that 1 second (bytes/packets/etc)
		"""
		st = int(open('/sys/class/net/{0}/statistics/{1}'.format(dev, inf)).read())
		sleep(1)
		return int(open('/sys/class/net/{0}/statistics/{1}'.format(dev, inf)).read()) - st

	def genJSON(self):
		for device in self.devices:
			for stat in self.stats:
				self.data[0][device][stat] = self.data[0][device][stat][1:]+(self.getstat(stat, device), )
		with open(self.JSONfile, 'w') as jsonfile:
			jsonfile.write( json.dumps(self.data) )


if __name__ == "__main__":
	x = stats()
	x.genJSON()


###############################
def sizeof_fmt(num, bit=False):
	""" (deprecated)
	Convert to human readable format
	"""
	y = ['bit/s','Kb/s','Mb/s','Gb/s','Tb/s'] if bit else ['bytes/s','KB/s','MB/s','GB/s','TB/s']
	for x in y:
		if num < 1024.00:
			return "%3.2f %s" % (num*8 if bit else num, x)
		num /= 1024.00


