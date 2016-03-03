import os,sys
import traceback
import logging
import time
import socket
import pickle
import signal
import select

from printrun.pronsole import pronsole
from printrun.utils import format_duration
from myMTCAdapter import *
from printrun import gcoder

def timeoutHandler(signum, frame):
        print "timeout!"
        raise Exception()

class requestHandler:
        def __init__(self):
                self.interp = pronsole()
                self.printing_on = 0
                self.adapter = myMTCAdapter("ultimaker", self.interp, self.printing_on)

        def processRequest(self,command):
                if (command == "poll"):
                        data = self.adapter.pollDevice()
                        #fp = open("tempData.pkl","wb")
                        #pickle.dump(data,fp)
                        #fp.flush()
                        with open("tempData.pkl","wb") as fp:
                                pickle.dump(data,fp)
                        print data
                        #return data


if __name__ == "__main__" :
        global currentHandler
        currentHandler = requestHandler()
        print "this is a test"
        signal.signal(signal.SIGALRM, timeoutHandler)
        currentHandler.interp.parse_cmdline(sys.argv[1:])
        #printing_on = 0
        currentHandler.interp.onecmd("connect")
        time.sleep(5)
        s = socket.socket()        
        host = '131.151.115.90'# ip of raspberry pi 
        print("Socket successfully created")
        port = 12345
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host,port))
        print("socket binded")
        command = ""
        s.listen(5)
        print("socket is listening")            
        s.setblocking(0)
                   
        while True :
                try:
                    ready = select.select([s],[],[],0.5)
                    if ready[0]:
                        c, addr = s.accept()     
                        print ('Got connection from', addr)
                        #data = input("Enter data to be sent: ")
                        #send a thank you message to the client. 
                        #c.send(("Thank you for connecting").encode('utf-8'))
                        try:
                                command = (c.recv(1024)).decode('utf-8')
                                print command
                                print " Command received. Processing ..."
                                if (command == 'probe'):
                                        print("Ultimaker 2,Ultimaker,3D printer,PLA,230,225,205,Square,USB")
                                elif (command == 'status'):
                                        if currentHandler.interp.p.printing:
                                                print("1")
                                        else:
                                                print("0")
                                elif ("load" in command):
                                        #file = command.split()
                                        #print file
                                        #fileName = "/home/pi/MyApp/" + file[1]
                                        #print fileName
                                        f = open('/home/pi/3dpAdapter/current_print.gco','wb')
                                        #f = open('/home/pi/MyApp/current_print.stl','wb')
                                        c.send('1')#ready to receive
                                        #cs, addr = s.accept()
                                        time.sleep(1)
                                        l = c.recv(1024)
                                        while (l) :
                                                print "receiving..."
                                                f.write(l)
                                                l = c.recv(1024)
                                                #print l
                                        f.close()
                                        print "Done receiving."
                                        currentHandler.processRequest("poll")
                                        time.sleep(5)
                                        #currentHandler.interp.onecmd('slice current_print.stl')
                                        currentHandler.interp.onecmd('load current_print.gco')
                                        #print(currentHandler.interp.message)
                                        if not currentHandler.interp.fgcode:
                                                print "No file loaded"
                                                #return
                                                continue
                                        
                                        #currentHandler.interp.onecmd("move x 100")
                                        #currentHandler.processRequest("poll")
                                        #time.sleep(5)
                                        #currentHandler.processRequest("poll")
                                        #currentHandler.interp.onecmd("move y -100")
                                        #time.sleep(5)
                                        #currentHandler.processRequest("poll")
                                        #currentHandler.interp.onecmd("move z -218 5000")
                                        #time.sleep(5)
                                        currentHandler.printing_on = 1
                                        #currentHandler.interp.p.printing = True
                                        
                                        currentHandler.processRequest("poll")
                                        currentHandler.interp.onecmd("settemp 210")
                                        #currentHandler.interp.onecmd("bedtemp 60")
                                        time.sleep(5)
                                        
                                        while (currentHandler.interp.status.extruder_temp <= currentHandler.interp.status.extruder_temp_target) :
                                                currentHandler.processRequest("poll")
                                                print "Raising temperature"
                                                currentHandler.interp.onecmd("gettemp")
                                                time.sleep(5)
                                        print "Target temperature is reached. Commencing print..."
                                        currentHandler.processRequest("poll")
                                        time.sleep(1)
                                        currentHandler.interp.onecmd("print")
                                        #print(",~#Printing has been started.#~,")
                                        print("1")
                                        
                
                                elif ("sdprint" in command):#need editing
                                        currentHandler.interp.onecmd("move y -100")
                                        time.sleep(5)
                                        currentHandler.interp.onecmd("move x 100")
                                        time.sleep(5)
                                        currentHandler.interp.onecmd("move z -218 5000")
                                        time.sleep(5)
                                        currentHandler.interp.onecmd("settemp 210")
                                        currentHandler.interp.onecmd("bedtemp 60")
                                        time.sleep(5)
                                        while (currentHandler.interp.status.extruder_temp <= currentHandler.interp.status.extruder_temp_target or currentHandler.interp.status.bed_temp <= currentHandler.interp.status.bed_temp_target) :
                                                print "Raising temperature"
                                                currentHandler.interp.onecmd("gettemp")
                                                time.sleep(5)
                                        print "Target temperature is reached. Commencing print..."
                                        time.sleep(1)
                                        currentHandler.interp.onecmd(command)
                                        #print(",~#Printing has been started.#~,")
                                        print("1")
                                        
                                elif (command == "lp"):
                                        currentHandler.interp.onecmd('load Asa.gcode')
                                        #print(currentHandler.interp.message)
                                        if not currentHandler.interp.fgcode:
                                                print "No file loaded"
                                                continue
                                        time.sleep(10)
                                        printing_on = 1
                                        currentHandler.interp.onecmd("print")
                                        #print(",~#Printing has been started.#~,")
                                        print("1")
                                                        
                
                                elif (command == "print"): #need editing
                                        currentHandler.interp.onecmd("settemp 210")
                                        currentHandler.interp.onecmd("bedtemp 60")
                                        time.sleep(5)
                                        while (currentHandler.interp.status.extruder_temp <= currentHandler.interp.status.extruder_temp_target or currentHandler.interp.status.bed_temp <= currentHandler.interp.status.bed_temp_target) :
                                                print "Raising temperature"
                                                currentHandler.interp.onecmd("gettemp")
                                                time.sleep(5)
                                        print "Target temperature is reached. Commencing print..."
                                        time.sleep(1)
                                        currentHandler.interp.onecmd(command)
                                        #print(",~#Printing has been started.#~,")
                                        print("1")
                                elif (command == "reset"):
                                        currentHandler.interp.onecmd("home")    
                                elif (command == "stop"): 
                                        currentHandler.interp.onecmd("pause")
                                        currentHandler.interp.onecmd("off")
                                        time.sleep(2)
                                        currentHandler.interp.onecmd("home")
                                        #print(",~#Printing has been canceled by user.#~,")
                                        print("1")
                                #monitoring
                                elif (command == "monitor"): #need editing
                                        preface = ""
                                        progress = 0
                                        if currentHandler.interp.p.printing:
                                                preface = _("Print progress: ")
                                                progress = 100 * float(currentHandler.interp.p.queueindex) / len(currentHandler.interp.p.mainqueue)
                                        elif currentHandler.interp.sdprinting:
                                                preface = _("Print progress: ")
                                                progress = currentHandler.interp.percentdone
                                        prev_msg = preface + "%.1f%%" % progress 
                                        temp_msg = "\nHotend: %s/%s\nBed: %s/%s" % (currentHandler.interp.status.extruder_temp, currentHandler.interp.status.extruder_temp_target,currentHandler.interp.status.bed_temp, currentHandler.interp.status.bed_temp_target)
                                        print('%.1f%%,%s,%s,#' % (progress,currentHandler.interp.status.extruder_temp,currentHandler.interp.status.bed_temp))
                                
                                elif (command == "gettemp"):
                                        if (currentHandler.interp.p.online):
                                                #print(",~#Hotend: %s/%s\nBed: %s/%s#~," % (currentHandler.interp.status.extruder_temp, currentHandler.interp.status.extruder_temp_target,currentHandler.interp.status.bed_temp, currentHandler.interp.status.bed_temp_target))
                                                print('%s,%s' % (currentHandler.interp.status.extruder_temp,currentHandler.interp.status.bed_temp))
                                        else :
                                                print(",~#No printer is connected. Connect to a printer first.#~,")
                                
                                else :
                                        #print("Not a valid command!")
                                        currentHandler.interp.onecmd(command)
                
                        except Exception, exc:
                                print exc
                        
                        #storing values in the temp file
                        currentHandler.processRequest("poll")
                        
                        if currentHandler.printing_on == 1 and not currentHandler.interp.p.printing:
                                currentHandler.printing_on = 0
                                time.sleep(2)
                                currentHandler.processRequest("home")
                                time.sleep(2)
                                currentHandler.processRequest("settemp 0")
                                time.sleep(2)
                                currentHandler.processRequest("bedtemp 0")
                                try:
                                        os.remove('current_print.gco')
                                except:
                                        pass
                    currentHandler.processRequest("poll")
                except KeyboardInterrupt:       
                        s.close()
                        print "Connection terminated. Thank you."       
                        sys.exit()      
                except socket.error,select.error:
                        s.close()
                        s = socket.socket()        
                        host = '130.184.104.182'# ip of raspberry pi 
                        print("Socket successfully created")
                        port = 12345
                        s.bind((host,port))
                        print("socket binded")
                        s.listen(5)
                        print("socket is listening")
                        s.setblocking(0)
                
