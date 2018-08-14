from wifi import Cell

import sys
import argparse

import sh

#configs for all the things
from config.config import MACS
from config.config import SSIDS
from config.config import PASSWORDS 
from config.config import DEFAULTS

def scanner(do_brute, interface):
	'''
	look for all the ap's
	'''
	#print MACS
	#print SSIDS
	#print PASSWORDS
	connections = []
	aps = sh.iwlist(interface, 'scan').split('Cell ')
	for ap in aps:
		#print ap
		for line in ap.splitlines():
			#print 'line: ', line
			if line.find('Address: ') > -1:
				#serach for our macs int the list
				print 'address:', line
				if any(s in line for s in MACS):
					print 'found camera by MAC address!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
					connections.append(ap)
			if line.find('ESSID') > -1:
				#serach for our ssids in the list
				print line 
				if any(s in line for s in SSIDS):
					print 'found camera by SSID!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
					connections.append(ap)
	#
	#this isnt working so lets print out
	#the default password for each 
	#connection we found
	#
	conn = list(set(connections))
	if len(conn) < 1:
		print 'nothing found'
		return
	#print conn
	print 'searching for defaults...'
	for key, value in DEFAULTS.iteritems():
		#print key
		for v in value:
			if str(conn).find(v) > -1:
				print '\tdevice type:', value[0]
				print '\tssid fingerprint:', value[1]
				print '\tmac ident:', value[2]
				print '\tdefault pass:', key
				print '\tfound value in conn:', v
				break

	if do_brute:
		print 'attempting to bruteforce logon of AP'
		conn = list(set(connections))
		for c in conn:
			ssid = c.split('ESSID:"')[1].split('"')[0]
			for pas in PASSWORDS:
				print '\t trying', ssid, 'with password', pas 
				#
				#This isnt working right now because kali, ubuntu
				#my variouse nic's, wpa_supplicant and network-manager
				#all hate me.... Fix me when I get a nic thats worth a 
				#damn
				#	
	return 

	



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-b', '--brute', action='store_true', help='brute force login of camera ap')
	parser.add_argument('-i', '--interface', action='store', help='the interface to use (required)', required=True)
	#add argument for external password list
	args = parser.parse_args()
	
	#do root check		
	if  sh.id().find('root') < 0:
		print 'you must be root, try again'
		sys.exit(0)
	
	if args.brute:
		scanner(True, args.interface)
	else:
		scanner(False, args.interface)	



if __name__ == '__main__':
	main()

