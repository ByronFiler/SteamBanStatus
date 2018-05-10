## Module for Manageing Files ##
## By Byron Filer ##

import vanityResolver

## Working as intended ##
def manageFilesVanityIDs():
	file0 = open('id.txt', 'r')

	file0_contents = file0.read()
	file0_contents = file0_contents.split()

	file0.close()

	if file0_contents != []:

		file0 = open("id.txt", 'w')
		file0.write('')
		file0.close()

		return file0_contents

	else:
		return []


def readConvert():
	file0 = open('64.txt', 'r')
	steam64 = []
	file0_contents = file0.read()
	file0_contents = file0_contents.split()

	for i in range(len(file0_contents)):
		steam64.append(file0_contents[i].split('/'))

	return steam64