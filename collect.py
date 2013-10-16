#!/usr/bin/env python
from time import sleep

def getstat(inf='rx_packets', dev='eth0'):
	st = int(open('/sys/class/net/{0}/statistics/{1}'.format(dev, inf)).read())
	sleep(1)
	return int(open('/sys/class/net/{0}/statistics/{1}'.format(dev, inf)).read()) - st

def sizeof_fmt(num, byte=False):
	y = ['bit/s','Kb/s','Mb/s','Gb/s','Tb/s'] if byte else ['bytes/s','KB/s','MB/s','GB/s','TB/s']
	for x in y:
		if num < 1024.00:
			return "%3.2f %s" % (num*8 if byte else num, x)
		num /= 1024.00

# Show Kb not KB
byte = False

while True:
	print "rx:\t{0}\ttx:\t{1}".format(sizeof_fmt(getstat('rx_bytes', 'eth0'), byte), sizeof_fmt(getstat('tx_bytes', 'eth0'), byte))

	#print "{0} kbit/s {1} p/s".format(rx_bytes()/128, rx_packets())
