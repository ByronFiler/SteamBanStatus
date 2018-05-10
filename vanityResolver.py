## Resolve Custom IDs ##
## By Byron Filer ##

import urllib.request # Send http requests
import json # Parse json
import time # Delay
import sys # Exit

API_KEY = 'put your api key here'

# Pass array of vanity IDs and it will return 64 Ids
def vanityIdResolver(vanityIdArray):
	steam64 = []
	for i in range(len(vanityIdArray)):
		responce = None # Has to be declared before the rest
		try:
			responce = urllib.request.urlopen('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=' + API_KEY + '&vanityurl=' + vanityIdArray[i]).read()
		except Exception as ex:
			print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n-= HTTP Request failed to connect. -=-\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
			raise ex
			sys.exit(-1)

		responce = responce.decode("utf-8", "ignore")
		responce = json.loads(responce)

		steam64.append((responce['response']['steamid'], vanityIdArray[i]))

	return steam64

# Reads the file and takes the custom generated mix
def mergeArrays(custom64):
	_ = open('64.txt', 'r')
	steam64Process_ = _.read()
	_.close()

	steam64Process_ = steam64Process_.split()
	steam64Process = []
	for i in range(len(steam64Process_)):
		steam64Process_[i] = steam64Process_[i].split('/')
		steam64Process.append(steam64Process_[i][0])

	steam64Process2 = []
	for i in range(len(custom64)):
		steam64Process2.append(custom64[i][0])

	return steam64Process + steam64Process2