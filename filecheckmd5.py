import md5, sys, os, time

def compute( filename, chunk = 2**20 ):
     file = open( filename, 'rb' )
     try:
         check = md5.new()
         data = file.read( chunk )
         count = 1
         while data:
             check.update( data )
             data = file.read( chunk )
         return check.hexdigest()
     except:
         print 'stopped at', file.tell()

def save( sum, filename ):
     target = filename + '.md5'
     open(target, 'w').write(sum)
     print 'writing md5 file complete'

if __name__ == "__main__":
     import sys
     t = time.time()
     print 'checking file', sys.argv[1]
     value = compute( sys.argv[1] )
     # save(value, sys.argv[1])
     t = time.time()-t
     print "time %s value %s"%( t, value)