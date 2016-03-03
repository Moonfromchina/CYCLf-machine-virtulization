import os,sys
import traceback
import logging
import time
import socket
from printrun.pronsole import pronsole
from printrun.utils import format_duration
from myMTCAdapter import *
from printrun import gcoder
if __name__ == "__main__" :
	interp = pronsole()
	print "this is a test"
	adapter = myMTCAdapter("ultimaker",interp)
	interp.parse_cmdline(sys.argv[1:])
	printing_on = 0
	interp.onecmd("connect")
	time.sleep(5)
	command = ""
	while True :
		command = raw_input("Enter command here: ")
		if (command == "disconnect"):
			#print(("Disconnecting printer. Please wait ...").encode('utf-8'))
			interp.onecmd(command)
			time.sleep(5)
			if not interp.p.online :
				#print(",~#Printer is now offline.#~,")
				print("1")
			else :
				#print(",~#Cannot disconnect. Please try again after a while#~,")
				print("0")
				
		elif(command == "poll"):
			print(adapter.pollDevice())
		elif (command == "pos"):
			#interp.userm114+=1
			print (interp.recvcb("ok C:"))
		elif (command == 'probe'):
			print("Ultimaker 2,Ultimaker,3D printer,PLA,230,225,205,Square,USB")
		elif (command == 'status'):
			if interp.p.printing:
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
			interp.onecmd('slice current_print.stl')
			interp.onecmd('load current_print_export.gcode')
			#print(interp.message)
			if not interp.fgcode:
				print "No file loaded"
				continue
			interp.onecmd("move x 100")
			time.sleep(5)
			interp.onecmd("move y -100")
			time.sleep(5)
			interp.onecmd("move z -218 5000")
			time.sleep(5)
			interp.onecmd("settemp 210")
			interp.onecmd("bedtemp 60")
			time.sleep(5)
			
			while (interp.status.extruder_temp <= interp.status.extruder_temp_target or interp.status.bed_temp <= interp.status.bed_temp_target) :
				print "Raising temperature"
				interp.onecmd("gettemp")
				time.sleep(5)
			print "Target temperature is reached. Commencing print..."
			time.sleep(10)
			printing_on = 1
			interp.onecmd("print")
			#print(",~#Printing has been started.#~,")
			print("1")
			

		elif ("sdprint" in command):#need editing
			interp.onecmd("move y -100")
			time.sleep(5)
			interp.onecmd("move x 100")
			time.sleep(5)
			interp.onecmd("move z -218 5000")
			time.sleep(5)
			interp.onecmd("settemp 210")
			interp.onecmd("bedtemp 60")
			time.sleep(5)
			while (interp.status.extruder_temp <= interp.status.extruder_temp_target or interp.status.bed_temp <= interp.status.bed_temp_target) :
				print "Raising temperature"
				interp.onecmd("gettemp")
				time.sleep(5)
			print "Target temperature is reached. Commencing print..."
			time.sleep(1)
			interp.onecmd(command)
			#print(",~#Printing has been started.#~,")
			print("1")
			
		
		elif (command == "print"): #need editing
			interp.onecmd("settemp 210")
			interp.onecmd("bedtemp 60")
			time.sleep(5)
			while (interp.status.extruder_temp <= interp.status.extruder_temp_target or interp.status.bed_temp <= interp.status.bed_temp_target) :
				print "Raising temperature"
				interp.onecmd("gettemp")
				time.sleep(5)
			print "Target temperature is reached. Commencing print..."
			time.sleep(1)
			interp.onecmd(command)
			#print(",~#Printing has been started.#~,")
			print("1")
			
		elif (command == "stop"): 
			interp.onecmd("pause")
			interp.onecmd("off")
			time.sleep(2)
			interp.onecmd("home")
			#print(",~#Printing has been canceled by user.#~,")
			print("1")
		#monitoring
		elif (command == "monitor"): #need editing
			preface = ""
			progress = 0
			if interp.p.printing:
				preface = _("Print progress: ")
				progress = 100 * float(interp.p.queueindex) / len(interp.p.mainqueue)
			elif interp.sdprinting:
				preface = _("Print progress: ")
				progress = interp.percentdone
			prev_msg = preface + "%.1f%%" % progress 
			temp_msg = "\nHotend: %s/%s\nBed: %s/%s" % (interp.status.extruder_temp, interp.status.extruder_temp_target,interp.status.bed_temp, interp.status.bed_temp_target)
			print('%.1f%%,%s,%s,#' % (progress,interp.status.extruder_temp,interp.status.bed_temp))
		
		elif (command == "gettemp"):
			if (interp.p.online):
				#print(",~#Hotend: %s/%s\nBed: %s/%s#~," % (interp.status.extruder_temp, interp.status.extruder_temp_target,interp.status.bed_temp, interp.status.bed_temp_target))
				print('%s,%s' % (interp.status.extruder_temp,interp.status.bed_temp))
			else :
				print(",~#No printer is connected. Connect to a printer first.#~,")
		
		elif (command == 'close'):
			print("Connection terminated!")
			break
		else :
			#print("Not a valid command!")
			interp.onecmd(command)
		if printing_on == 1 and not interp.p.printing:
			printing_on = 0
			interp.onecmd("home")
			time.sleep(1)
			interp.onecmd("settemp 0")
			interp.onecmd("bedtemp 0")
			os.remove('current_print.gco')
		   
			
