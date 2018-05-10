import urllib.request
import json
import socket
API_KEY = 'Put your api key here'

def gatherAccountInformation(steam64Ids):

	response0, response1, response2 = None, None, None # Needs to be declared earlier to be updated in try catch

	# Request general account data
	try:
		response0 = urllib.request.urlopen('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + API_KEY + '&steamids=' + (',').join(steam64Ids)).read() # Sends the API request with all the details
		response0 = response0.decode("utf-8", "ignore")
		response0 = json.loads(response0)
	
	except Exception as ex:
		print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n-= HTTP Request failed to connect. -=-\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
		raise ex
		sys.exit(-1)

	# Request ban status
	try:
		response1 = urllib.request.urlopen('http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=' + API_KEY + '&steamids=' + (',').join(steam64Ids)).read() 
		response1 = response1.decode("utf-8", "ignore")
		response1 = json.loads(response1)
	
	except Exception as ex:
		print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n-= HTTP Request failed to connect. -=-\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n')
		raise ex

	response0_ = response0['response']['players'] # List containing dicts, which contain the data
	respones1_ = response1['players']

	response0_Processed, response1_Processed = [], []
	
	for i in response0_:
		response0_Processed_ = []
		response0_Processed_.append(str(i['personaname']))
		response0_Processed_.append(str(i['profileurl']))
		response0_Processed_.append(str(i['steamid']))
		response0_Processed.append(response0_Processed_)

	for i in respones1_:
		response1_Processed_ = []
		response1_Processed_.append(str(i['VACBanned']))
		response1_Processed_.append(str(i['DaysSinceLastBan']))
		response1_Processed_.append(str(i['NumberOfGameBans']))
		response1_Processed_.append(str(i['SteamId']))
		response1_Processed.append(response1_Processed_)


	response0_Processed = sorted(response0_Processed, key=lambda x: x[2], reverse=True) # Sorts it
	response1_Processed = sorted(response1_Processed, key=lambda x: x[3], reverse=True) # Sorts it

	finalSteamArray = []

	for i in range(len(response1_Processed)):
		response0_Processed[i].pop(2) # Removeing 64 Id now joined
		response1_Processed[i].pop(3) # Same, different pos

		## Cleans the steam url and just gets vanity ID
		steamUrlTemp = response0_Processed[i][1]
		steamUrlTemp = steamUrlTemp.split('/')
		if steamUrlTemp[len(steamUrlTemp) -3] == 'profiles':
			response0_Processed[i][1] = '---' # If they have no vanity URL
		else:
			steamUrlTemp = steamUrlTemp[len(steamUrlTemp) -2]
			response0_Processed[i][1] = steamUrlTemp

		finalSteamArray.append([response0_Processed[i][0], response0_Processed[i][1], response1_Processed[i][0], response1_Processed[i][1], response1_Processed[i][2]])

	return finalSteamArray