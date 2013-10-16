#!/usr/bin/env python
from time import sleep
import json

class stats:
	def __init__(self):
		self.JSONfile = './www/stats.json'
		
	def createDB(self):
		"""
		"""
		
def getstat(inf='rx_packets', dev='eth0'):
	"""
	Compare information 1 second apart
	to see how much was transferred within that 1 second (bytes/packets/etc)
	"""
	st = int(open('/sys/class/net/{0}/statistics/{1}'.format(dev, inf)).read())
	sleep(1)
	return int(open('/sys/class/net/{0}/statistics/{1}'.format(dev, inf)).read()) - st

def sizeof_fmt(num, bit=False):
	""" (deprecated)
	Convert to human readable format
	"""
	y = ['bit/s','Kb/s','Mb/s','Gb/s','Tb/s'] if bit else ['bytes/s','KB/s','MB/s','GB/s','TB/s']
	for x in y:
		if num < 1024.00:
			return "%3.2f %s" % (num*8 if bit else num, x)
		num /= 1024.00

R_LENGTH = 2
# Create empty tuples with the length of R_LENGTH
data = [ { # Let this structure be created by `devices`	and `stats`
			'rx_bytes':		((0,)*R_LENGTH),
			'tx_bytes':		((0,)*R_LENGTH),
			'rx_packets':	((0,)*R_LENGTH),
			'tx_packets':	((0,)*R_LENGTH)
		 },
		 {
			'':''		 
		 }
		]

#data[0]['rx_bytes'] = data[0]['rx_bytes'][1:]+(13,)
print json.dumps(data)



devices = ['eth0']
stats = ['rx_bytes', 'tx_bytes', 'rx_packets', 'tx_packets']
#bit = False
exit()
for device in devices:
	for stat in stats:
		data[0][stat] = data[0][stat][1:]+(getstat(stat, device), )


# Show Kb not KB
#
#while True:
#	print "rx:\t{0}\ttx:\t{1}".format(sizeof_fmt(getstat('rx_bytes', 'eth0'), byte), sizeof_fmt(getstat('tx_bytes', 'eth0'), byte))
#
#	#print "{0} kbit/s {1} p/s".format(rx_bytes()/128, rx_packets())
#


