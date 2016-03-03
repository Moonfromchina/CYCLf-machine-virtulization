import urllib
import time

r = urllib.urlopen('http://130.184.104.40:1080/sample')
start = time.time() * 1000
page = r.read()
end = time.time() * 1000
r.close()
p = end - start
print p