import BaseHTTPServer
import time
from datetime import datetime
import socket
import json
import sys
import threading

from printerAdapter import *
from printrun.pronsole import pronsole

# Default IP and Port settings.
HOST_NAME = '127.0.0.1'
PORT_NUMBER = 1080

interp = pronsole()

""" Webserver classes. """

# @class: requestHandler
class requestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # end createMTCHook
    # @function: do_HEAD
    def do_HEAD(s):
        # Send a success response.
        s.send_response(200)
        # Send the content type.
        s.send_header("Content-type", "text/xml")
        # End the headers.
        s.end_headers()
    # end do_HEAD
    
    # @function: do_GET
    def do_GET(s):
        # Send the header information (success, content type)
        s.send_response(200)
        s.send_header("Content-type", "text/xml")
        s.end_headers()
        #printerData = None
        try:
            # Split up the path to be easier to parse or analyze.
            splitPath = s.path.split("?")
            # Grab the command, possibly the machine name too.
            command = splitPath[0]
	    print "1 "+command
            # Grab the parameters.
            params = None
            if len(splitPath) > 1:
                params = splitPath[1]
            # end if

            # Take off the leading "/".
            command = command.lstrip("/")
	    print "2 "+command
            # If the command contains a "/".
            if "/" in command:
                # Split on that character
                splitCommand = command.split("/")
                # The first parameter will be the specified device.
                #specifiedDevice = splitCommand[0]
                # The command is the second element.
                command = splitCommand[0]
            # end if
	    print "3 "+command	
            if "poll" in command:
		print "success"
		adapter = printerAdapter(interp)
		printerData = adapter.pollDevice()
		print printerData
		s.wfile.write("<html><body><h1>"+printerData+"</h1></body></html>")
	# end try
        except Exception as ex:
            # If an error occurred, write it.
            error = traceback.format_exc(sys.exc_info()[2])
            s.wfile.write(error)
        # end except
        
        # Write the content to the page.
	#s.wfile.write(printerData)
        #s.wfile.write("\t<body>\n\t\t<p>Just testing web serving.</p>")
        #s.wfile.write("\t\t<p>Page path: "+s.path+"</p></body>\n</html>")
    # end do_GET
# end requestHandler

if __name__ == '__main__':

    print "this is a test"
    interp.parse_cmdline(sys.argv[1:])
    interp.onecmd("connect")
    time.sleep(5)
    interp.onecmd("gettemp")
    time.sleep(2)
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), requestHandler)
    #print time.asctime() + "Server starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        agent.isRunning = False
        pass
    
    httpd.server_close()
    #print time.asctime() + "server stops - %s:%s" % (HOST_NAME, PORT_NUMBER)