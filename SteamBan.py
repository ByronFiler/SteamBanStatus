## Final Edition of Steam Ban Status ##

## TODO
## Allow to sort by game bans ie shortest to longest
## Sort by ban type, vacs together, games together, vac and game together and nones togethers
## Sort by URL
## Sort by display name

import sys
import time

_startTime = time.time()

# My Modules
import vanityResolver
import manageFiles
import accountInformation

API_KEY = 'put your api key here' # API Key for main account

## Resolving user request, on what they enter for name, url, days
try:
	sys.argv[1]
except IndexError:
	try:
		file = open('default.txt', 'r')
		sys.argv.append(file.read())
		file.close()
	except FileNotFoundError:
		file = open('default.txt', 'w')
		file.close()
		sys.argv.append('None')

# Cleans file for a new log
logFile = open('log.txt', 'w')
logFile.write('')
logFile.close()

# Leaves log file open to be used throughout the program
logFile = open('log.txt', 'a')

## -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= RESOLVING VANITY IDS -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

steamVanityIds = manageFiles.manageFilesVanityIDs() # Vanity IDs from file

if steamVanityIds != []:
	logFile.write('[' + time.strftime('%H:%M:%S') + '] Aquired ' + str(len(steamVanityIds)) + ' new vanity ID(s) to be processed\n')
else:
	logFile.write('[' + time.strftime('%H:%M:%S') + '] No new vanity IDs found, none needed to be processed.\n')

if steamVanityIds != []:
	steam64Id_0 = vanityResolver.vanityIdResolver(steamVanityIds) # Resolves vanity IDs
	logFile.write('[' + time.strftime('%H:%M:%S') + '] Successfully resolved all vanity IDs via Steam API\n')

else:
	steam64Id_0 = [] # If there are no custom Ids it's fine

steam64Id_1 = manageFiles.readConvert() # Converts 64 File into readable format for export and processing
logFile.write('[' + time.strftime('%H:%M:%S') + '] Successfully read file for 64 IDs, and processed it.\n')

steam64Id = steam64Id_0 + steam64Id_1 # Combines arrays

file = open('64.txt', 'w') # Specify w so overwrites data already in the file
steam64IdExport = steam64Id[:] # [:] needed otherwise it creates a reference that will overwrite

for i in range(len(steam64IdExport)):
	steam64IdExport[i] = ('/').join(steam64IdExport[i])
steam64IdExport = ('\n').join(steam64IdExport)

file.write(steam64IdExport)
file.close()
logFile.write('[' + time.strftime('%H:%M:%S') + '] Successfully updated steam 64 Ids file, and cleaned vanity IDs file, now they have been processed.\n')

for i in range(len(steam64Id)):
	steam64Id[i] = steam64Id[i][0] # Cleans up the array

## -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

## -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-PROCESSING FOR OUTPUT -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
fullAccountDetails = accountInformation.gatherAccountInformation(steam64Id)
logFile.write('[' + time.strftime('%H:%M:%S') + '] All account information needed Successfully requested and processed from Steam API\n')


lengthOfSteamName = [12] # Account Name , len is 12
lengthOfSteamUrl = [10] # Vanity Url , len is 10
lengthOfDaysSinceLastBan = [20] # Days Since Last Ban , len is 19
lengthOfBanType = [9] # Ban Type , len is 8

# This is used to sort the output based on a specific feature on a user request for output
if sys.argv[1].lower() == 'name':
	fullAccountDetails = sorted(fullAccountDetails, key=lambda x: x[0], reverse=True)
	logFile.write('[' + time.strftime('%H:%M:%S') + '] User detected as requesting to sort by name, done.\n')
elif sys.argv[1].lower() == 'url':
	fullAccountDetails = sorted(fullAccountDetails, key=lambda x: x[1], reverse=True)
	logFile.write('[' + time.strftime('%H:%M:%S') + '] User detected as requesting to sort by url, done.\n')
elif sys.argv[1].lower() == 'days':
	fullAccountDetails = sorted(fullAccountDetails, key=lambda x: int(x[3]), reverse=False)
	logFile.write('[' + time.strftime('%H:%M:%S') + '] User detected as requesting to sort by days, done.\n')
else:
	logFile.write('[' + time.strftime('%H:%M:%S') + '] No user sorting request recieved, output will be random.\n')

for i in range(len(fullAccountDetails)):
	lengthOfSteamName.append(len(fullAccountDetails[i][0]))
	lengthOfSteamUrl.append(len(fullAccountDetails[i][1]))
	lengthOfDaysSinceLastBan.append(len(str(fullAccountDetails[i][3])))

	## [0] = Name of the account in display
	## [1] = Vanity Url
	## [2] = Vac ban 'True' or 'False'
	## [3] = Number of Days since last ban
	## [4] = Number of game bans

	if fullAccountDetails[i][2] == 'False' and str(fullAccountDetails[i][4]) == '0':
		fullAccountDetails[i][3] = '-'

	if fullAccountDetails[i][2] == 'True' and str(fullAccountDetails[i][4]) != '0':
		fullAccountDetails[i][2] = 'VAC & Game Ban'
	elif str(fullAccountDetails[i][4]) != '0' and fullAccountDetails[i][2] != 'Flase':
		fullAccountDetails[i][2] = 'Game Ban'
	elif fullAccountDetails[i][2] == 'True' and str(fullAccountDetails[i][4]) == '0':
		fullAccountDetails[i][2] = 'VAC'
	elif fullAccountDetails[i][2] == 'False' and str(fullAccountDetails[i][4]) == '0':
		fullAccountDetails[i][2] = 'None'

	lengthOfBanType.append(len(fullAccountDetails[i][2]))

logFile.write('[' + time.strftime('%H:%M:%S') + '] Successfully processed all of the user information.\n')

if sys.argv[1].lower() == 'bans':
	fullAccountDetails = sorted(fullAccountDetails, key=lambda x: x[2], reverse=True)

lengthOfSteamName = max(lengthOfSteamName)
lengthOfSteamUrl = max(lengthOfSteamUrl)
lengthOfDaysSinceLastBan = max(lengthOfDaysSinceLastBan)
lengthOfBanType = max(lengthOfBanType)

print('Account Name' + (' ' * (int(lengthOfSteamName) - 12)) + ' | ' + 'Vanity Url' + (' ' * (int(lengthOfSteamUrl) - 10)) + ' | ' + 'Ban Type ' + (' ' * (int(lengthOfBanType) - 9)) + ' | ' + 'Days Since Last Ban ' + (' ' * (int(len(str(lengthOfDaysSinceLastBan)) - 20))) + ' |')
print(('-' * int(lengthOfSteamName)) + ('-' * int(lengthOfSteamUrl)) + ('-' * int(lengthOfDaysSinceLastBan)) + ('-' * int(lengthOfBanType)) + '-' * 11)

for i in range(len(fullAccountDetails)):
	print(fullAccountDetails[i][0] + (' ' * (int(lengthOfSteamName) - len(fullAccountDetails[i][0]))) + ' | ' + fullAccountDetails[i][1] + (' ' * (int(lengthOfSteamUrl) - len(fullAccountDetails[i][1]))) + ' | ' + str(fullAccountDetails[i][2]) + (' ' * int(lengthOfBanType - (len(str(fullAccountDetails[i][2]))))) + ' | ' + str(fullAccountDetails[i][3]) + (' ' * (lengthOfDaysSinceLastBan - len(str(fullAccountDetails[i][3])))) + ' | ')

logFile.write('[' + time.strftime('%H:%M:%S') + '] Data displayed, program complete.\n')
_endTime = time.time()
logFile.write('Program Executed in ' + str(round(_endTime - _startTime, 3)) + ' seconds')
logFile.close()
## -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
