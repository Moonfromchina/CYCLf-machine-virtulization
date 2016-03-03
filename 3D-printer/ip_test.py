#!/usr/bin/env python

# This file is part of the Printrun suite.
#
# Printrun is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Printrun is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Printrun.  If not, see <http://www.gnu.org/licenses/>.

import sys
import traceback
import logging
import time
import socket
from printrun.pronsole import pronsole

if __name__ == "__main__":

    interp = pronsole()
    print "This is a test"
    
    interp.parse_cmdline(sys.argv[1:])
    
    s = socket.socket()
    host = '130.184.104.175'
    port = 12345
    s.connect((host,port))
    print(s.recv(1024))
    s.send(("I am ready to play").encode('utf-8'))
    while True :
	cmnd = (s.recv(1024)).decode('utf-8')
	time.sleep(5)
	print 'Data received'
	print(cmnd)
	#time.sleep(3)
	interp.onecmd(cmnd)
