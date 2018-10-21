from soco import SoCo
import urllib
import argparse

class SonosQ:
	def __init__(self, address):
		self.ipAddress		= address
		self.zone			= SoCo(self.ipAddress)
		self.__replaceStringFlag = False
		
	def write_Q_as_m3u(self, filePath, ignoredFilePath = ""):
		playlistFile = open(filePath, "w")
		if ignoredFilePath <> None:
			ignoredFile = open(ignoredFilePath, "w")	
		
		i = 0
		myQ = self.zone.get_queue(start = i)
		while i < myQ.total_matches :
			myQ = self.zone.get_queue(start = i)
			for item in myQ:	
				i+=1
				try:
					strippedURI = self.uri2filepath(item.resources[0].uri)
				except:
					print("Unknown Item: " + str(item.__dict__))
				else:
					if strippedURI <> None:
						# print(strippedURI)
						encoded_URI = strippedURI#.decode('utf-8').encode('latin-1', 'replace')
						if self.__replaceStringFlag:
							encoded_URI = encoded_URI.replace(self.mainString, self.replacementString)
						playlistFile.write(encoded_URI + "\n")
					else:
						# print("No match found: " + str(item.__dict__))
						if ignoredFilePath <> None:
							ignoredFile.write(str(item.__dict__) + "\n")
			
	def enableStringReplace(self, mainString, replacementString):
		self.mainString = mainString
		self.replacementString = replacementString
		self.__replaceStringFlag = True
		
	def uri2filepath(self, uri):
		split_uri = uri.split(':')
		if split_uri[0] == "x-file-cifs": #We have a Local Library Item.
			myURI = split_uri[1]
			myURI = urllib.unquote(myURI)
			return myURI
		# else:
		# 	return uri
	
if __name__ == '__main__':
	# Getting and parsing the commandLine arguments
	parser = argparse.ArgumentParser(description='Export the queue or a playlist from your Sonos system. Only works for local library service.')
	parser.add_argument('ipAddress', type=str,
	                   help='Sonos IP Address')
	parser.add_argument('playlistFile',
	                   help='Path of the exported playlist file')
	parser.add_argument('-i', '--ignoredFile',
	                   help='Path of the file to write the ignored objects. (For debugging and/or advanced users only)')
	parser.add_argument('-r', '--replaceString', nargs=2, metavar=("MAINSTRING", "REPLACEMENT"),
	                   help='Replace a string in the exported lines')
	args = parser.parse_args()

	mySonosQ = SonosQ(args.ipAddress)
	if args.replaceString:
		mySonosQ.enableStringReplace(args.replaceString[0], args.replaceString[1])
	mySonosQ.write_Q_as_m3u(args.playlistFile, args.ignoredFile)
	
