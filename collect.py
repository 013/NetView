#!/usr/bin/env python
from time import sleep
import json
import threading

class stats:
	def __init__(self):
		self.JSONfile = './www/stats.json'
		self.history = 60
		# Find device names with `ifconfig` or `ip link show`
		self.devices = ['eth0', 'vmbr0']
		self.stats = ['rx_bytes', 'tx_bytes']#, 'rx_packets', 'tx_packets']
		"""
		collisions           rx_dropped           rx_missed_errors     tx_carrier_errors    tx_heartbeat_errors
		multicast            rx_errors            rx_over_errors       tx_compressed        tx_packets
		rx_bytes             rx_fifo_errors       rx_packets           tx_dropped           tx_window_errors
		rx_compressed        rx_frame_errors      tx_aborted_errors    tx_errors
		rx_crc_errors        rx_length_errors     tx_bytes             tx_fifo_errors
		"""
		
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
		(This function will probably get called thousands of times and it's open a file twice..........)
		"""
		st = int(open('/sys/class/net/{0}/statistics/{1}'.format(dev, inf)).read())
		sleep(1)
		return int(open('/sys/class/net/{0}/statistics/{1}'.format(dev, inf)).read()) - st
	
	def setVar(self, i, device, stat):
		self.data[i][device][stat] = self.data[i][device][stat][1:]+(self.getstat(stat, device), )
		
	def genJSON(self):
		i=0
		threads = []
		for device in self.devices:
			for stat in self.stats:
				t = threading.Thread(target=self.setVar, args=(i,device,stat))
				threads.append(t)
				t.start()
			i+=1
		for thread in threads:
			thread.join()
		# The JSON file is also getting rewritten every couple of seconds... disk thrashing??????
		with open(self.JSONfile, 'w') as jsonfile:
			jsonfile.write( json.dumps(self.data) )

if __name__ == "__main__":
	x = stats()
	#for i in range(x.history):
	# 
	while True:
		x.genJSON()

