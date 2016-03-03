import os,sys
import traceback
import logging
import time
import socket
import pickle
import signal

from printrun.pronsole import pronsole
from printrun.utils import format_duration
from myMTCAdapter import *
from printrun import gcoder

#currentHandler = None

def timeoutHandler(signum, frame):
	print "timeout!"
	raise Exception()

class requestHandler:
	def __init__(self):
		self.interp = pronsole()
		self.printing_on = 0
		self.adapter = myMTCAdapter("ultimaker", self.interp)

	def processRequest(self,command):
		if (command == "disconnect"):
			#print(("Disconnecting printer. Please wait ...").encode('utf-8'))
			self.interp.onecmd(command)
			time.sleep(5)
			if not self.interp.p.online :
				#print(",~#Printer is now offline.#~,")
				print("1")
			else :
				#print(",~#Cannot disconnect. Please try again after a while#~,")
				print("0")
				
		elif(command == "poll"):
			data = self.adapter.pollDevice()
			#fp = open("tempData.pkl","w")
			#pickle.dump(data,fp)
			print data
			return data
		elif (command == "pos"):
			#self.interp.userm114+=1
			print (self.interp.recvcb("ok C:"))
		elif (command == 'probe'):
			print("Ultimaker 2,Ultimaker,3D printer,PLA,230,225,205,Square,USB")
		elif (command == 'status'):
			if self.interp.p.printing:
				print("1")
			else:
				print("0")
		elif ("load" in command):
			#file = command.split()
			#print file
			#fileName = "/home/pi/MyApp/" + file[1]
			#print fileName
			#f = open('/home/pi/MyApp/current_print.gco','wb')
			f = open('/home/pi/MyApp/current_print.stl','wb')
			print('1')#ready to receive
			#cs, addr = s.accept()
			time.sleep(1)
			l = c.recv(1024)
			while (l) :
				print "receiving..."
				f.write(l)
				l = c.recv(1024)
			f.close()
			print "Done receiving."
			time.sleep(5)
			self.interp.onecmd('slice current_print.stl')
			self.interp.onecmd('load current_print_export.gcode')
			#print(self.interp.message)
			if not self.interp.fgcode:
				print "No file loaded"
				return
			self.interp.onecmd("move x 100")
			time.sleep(5)
			self.interp.onecmd("move y -100")
			time.sleep(5)
			self.interp.onecmd("move z -218 5000")
			time.sleep(5)
			self.interp.onecmd("settemp 210")
			self.interp.onecmd("bedtemp 60")
			time.sleep(5)
			
			while (self.interp.status.extruder_temp <= self.interp.status.extruder_temp_target or self.interp.status.bed_temp <= self.interp.status.bed_temp_target) :
				print "Raising temperature"
				self.interp.onecmd("gettemp")
				time.sleep(5)
			print "Target temperature is reached. Commencing print..."
			time.sleep(10)
			printing_on = 1
			self.interp.onecmd("print")
			#print(",~#Printing has been started.#~,")
			print("1")
			

		elif ("sdprint" in command):#need editing
			self.interp.onecmd("move y -100")
			time.sleep(5)
			self.interp.onecmd("move x 100")
			time.sleep(5)
			self.interp.onecmd("move z -218 5000")
			time.sleep(5)
			self.interp.onecmd("settemp 210")
			self.interp.onecmd("bedtemp 60")
			time.sleep(5)
			while (self.interp.status.extruder_temp <= self.interp.status.extruder_temp_target or self.interp.status.bed_temp <= self.interp.status.bed_temp_target) :
				print "Raising temperature"
				self.interp.onecmd("gettemp")
				time.sleep(5)
			print "Target temperature is reached. Commencing print..."
			time.sleep(1)
			self.interp.onecmd(command)
			#print(",~#Printing has been started.#~,")
			print("1")
			
		elif (command == "lp"):
			self.interp.onecmd('load Asa.gcode')
			#print(self.interp.message)
			if not self.interp.fgcode:
				print "No file loaded"
				return
			time.sleep(10)
			printing_on = 1
			self.interp.onecmd("print")
			#print(",~#Printing has been started.#~,")
			print("1")
					

		elif (command == "print"): #need editing
			self.interp.onecmd("settemp 210")
			self.interp.onecmd("bedtemp 60")
			time.sleep(5)
			while (self.interp.status.extruder_temp <= self.interp.status.extruder_temp_target or self.interp.status.bed_temp <= self.interp.status.bed_temp_target) :
				print "Raising temperature"
				self.interp.onecmd("gettemp")
				time.sleep(5)
			print "Target temperature is reached. Commencing print..."
			time.sleep(1)
			self.interp.onecmd(command)
			#print(",~#Printing has been started.#~,")
			print("1")
			
		elif (command == "stop"): 
			self.interp.onecmd("pause")
			self.interp.onecmd("off")
			time.sleep(2)
			self.interp.onecmd("home")
			#print(",~#Printing has been canceled by user.#~,")
			print("1")
		#monitoring
		elif (command == "monitor"): #need editing
			preface = ""
			progress = 0
			if self.interp.p.printing:
				preface = _("Print progress: ")
				progress = 100 * float(self.interp.p.queueindex) / len(self.interp.p.mainqueue)
			elif self.interp.sdprinting:
				preface = _("Print progress: ")
				progress = self.interp.percentdone
			prev_msg = preface + "%.1f%%" % progress 
			temp_msg = "\nHotend: %s/%s\nBed: %s/%s" % (self.interp.status.extruder_temp, self.interp.status.extruder_temp_target,self.interp.status.bed_temp, self.interp.status.bed_temp_target)
			print('%.1f%%,%s,%s,#' % (progress,self.interp.status.extruder_temp,self.interp.status.bed_temp))
		
		elif (command == "gettemp"):
			if (self.interp.p.online):
				#print(",~#Hotend: %s/%s\nBed: %s/%s#~," % (self.interp.status.extruder_temp, self.interp.status.extruder_temp_target,self.interp.status.bed_temp, self.interp.status.bed_temp_target))
				print('%s,%s' % (self.interp.status.extruder_temp,self.interp.status.bed_temp))
			else :
				print(",~#No printer is connected. Connect to a printer first.#~,")
		
		else :
			#print("Not a valid command!")
			self.interp.onecmd(command)

currentHandler = requestHandler()

if __name__ == "__main__" :
	#global currentHandler
	#currentHandler = requestHandler()
	print "this is a test"
	signal.signal(signal.SIGALRM, timeoutHandler)
	currentHandler.interp.parse_cmdline(sys.argv[1:])
	#printing_on = 0
	currentHandler.interp.onecmd("connect")
	time.sleep(5)
	command = ""
	while True :
		if currentHandler.interp.p.printing:
			signal.alarm(2)
		else:
			signal.alarm(20)
		try:
			command = raw_input("Enter command here: ")
			signal.alarm(0)
			currentHandler.processRequest(command)
			
		except Exception, exc:
			print exc
		
		#storing values in the temp file
		currentHandler.processRequest("poll")
		
		if currentHandler.printing_on == 1 and not currentHandler.interp.p.printing:
			currentHandler.printing_on = 0
			currentHandler.processRequest("home")
			time.sleep(1)
			currentHandler.processRequest("settemp 0")
			currentHandler.processRequest("bedtemp 0")
			os.remove('current_print.gco')
		   
			
