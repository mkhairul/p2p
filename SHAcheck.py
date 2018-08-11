import sha, sys, os, time

def compute(filename, chunk=2**20):
	file = open(filename, 'rb')
	try:
		check = sha.new()
		data = file.read(chunk)
		count = 1
		while data:
			check.update(data)
			data = file.read(chunk)
		return check.hexdigest()
	except:
		print 'stop at', file.tell()

def save(sum, filename):
	target = filename + '.SHA'
	open(target,'w').write(sum)
	print 'writing md5 file complete'

if __name__=="__main__":
	t = time.time()
	print 'checking file', sys.argv[1]
	value = compute(sys.argv[1])
	t = time.time()-t
	print "time %s value %s" % (t,value)	