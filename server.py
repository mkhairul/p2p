#!usr/bin/python
################
# module used socket(python), thread(python), filecheckmd5.py
################
# Authors:
# 	Mohd Khairul Anuar (kkmka90) - client.py, server.py
#	Mike C. Fletcher (comp.lang.python) 23/01/2002 - md5 checksum script
################

from socket import *
import thread

HOST = ''
PORT = 8578

def client(handlersock, address):

	size = handlersock.recv(1024)
	size = int(size)
	handlersock.send('received')
	
	filename = handlersock.recv(1024)
	f=open(filename, 'wb')
	print 'File - ',filename,' created ',size,'bytes'
	handlersock.send('received')

	crc = handlersock.recv(2048)
	print address,' - ',filename,'-',crc
	handlersock.send('received')
	
	chunkSize = 2048
	while size > 0:
		data = handlersock.recv(chunkSize)
		f.write(data)
		size = size - chunkSize
		handlersock.send("received")
	
	f.close()
	print filename,' transfer complete'

	# FILE CHECKSUM
	print 'checking file checksum'
	if (not filecheck(crc, filename)): 
		print filename,':  Error - mismatch'
	else:
		print filename,': Success - match'

	handlersock.close()
	print 'handler for - ', address, ' closed'

def filecheck(clienthash, filename):
	import filecheckmd5
	serverhash = filecheckmd5.compute(filename)
	tmp = cmp(clienthash, serverhash)
	if tmp == 0:
		return True
	else:
		return False

def serve():
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.bind((HOST, PORT))
	serversock.listen(2)
	print 'socket listening for connections...'
	while 1:
		handlersock, addr = serversock.accept()
		thread.start_new_thread(client,(handlersock,addr))
		print 'handler connected by', addr

if __name__ == '__main__':
	serve()	