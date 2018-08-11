#!usr/bin/python
################
# module used sys(python), os(python), socket(python), time(python), filecheckmd5.py, progressBar.py
################
# Authors:
# 	Mohd Khairul Anuar (kkmka90) - client.py, server.py
#	Randy Pargman (Activestate Python Cookbook) 2002/12/11 - progressBar.py
#	Mike C. Fletcher (comp.lang.python) 23/01/2002 - md5 checksum script
################

import sys
import os
from socket import *

def transfer(filename,HOST='localhost', PORT=8578):
	
	clientsock = socket(AF_INET, SOCK_STREAM)

	# CHECK FOR HOST AVAILABILITY.
	clientsock.settimeout(120)
	tmp = clientsock.connect_ex((HOST,PORT)) 
	if tmp != 0:
		sys.exit('Connection Timeout - 200sec')
	
	# SEND HOST FILESIZE.
	size = os.path.getsize(filename)
	size = str(size)
	clientsock.send(size)

	# WAIT FOR ACKNOWLEDGEMENT BEFORE PROCEED
	clientsock.recv(1024)

	# SEND FILE NAME TO SOCKET SERVER.
	# STRIP \ FROM FILEPATH STRING AND ASSIGN FILENAME
	# OR ELSE SERVER WONT SAVE IN THE SAME DIRECTORY
	# IT WILL SAVE IN THE SAME DIRECTORY AS THE FILEPATH.
	tmp = filename.split('\\')
	tmpFilename = tmp[len(tmp)-1]
	clientsock.send(tmpFilename)
	clientsock.recv(1024) # WAIT FOR ACK
	
	# FILE CHECKSUM MD5 - FASTER THEN SHA-1
	import filecheckmd5
	hash = filecheckmd5.compute(filename)
	clientsock.send(hash)
	print tmpFilename, '- md5 : ', hash
	clientsock.recv(1024) # ACK

	import time
	size = int(size)
	import progressBar
	temp = progressBar.progressBar(0, size)

	# FOR UPDATING PROGRESS BAR
	currentSize = 0 
	t = time.time()

	# CHECK TIME FOR ACK FROM HOST
	t2 = 0.0
	chunkSize = 2048
	try:  
		while size > 0:
			chunk = f.read(chunkSize)
			t2 = time.time()
			clientsock.send(chunk)
			size = size - chunkSize
			currentSize = currentSize + chunkSize
			temp.updateAmount(currentSize)
			clientsock.recv(1024) # WAIT FOR ACKNOWLEDGEMENT HOST
			speed = time.time() - t2
			print temp.progBar, currentSize,' out of ',temp.max," Chunk Travel - 2KB/%.5f sec" % (speed),"\r",
	except:
		sys.exit("Error - connection lost")

	t = time.time() - t
	print '\nTransfer Complete - took %s sec' % (t)
	print 'Close socket'
	clientsock.close()


if __name__=="__main__":
	if len(sys.argv) >= 4:
		filename = sys.argv[1]
		HOST = sys.argv[2]
		PORT = int(sys.argv[3])
	else:
		# FILENAME
		if len(sys.argv) < 2:
			filename = raw_input('filename/path ->')
			try:
				open(filename, 'rb')
			except:
				sys.exit("No such file")
		else:
			filename = sys.argv[1]
		if filename == '': sys.exit("Enter filename, proces Aborted")
		# HOST
		h = raw_input('host ->')
		if(h == ''): 
			HOST = 'localhost'
		else:
			HOST = h
		h = raw_input('port ->')
		if(h == ''): 
			PORT = 8578
		else:
			PORT = int(h)
	# CHECK IF FILE EXISTS.
	try:
		f = open(filename, 'rb')
	except:
		sys.exit("No such file, process Aborted")

	transfer(filename,HOST,PORT) # START