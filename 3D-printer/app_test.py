import os,sys
import traceback
import logging
import time
import socket
from printrun.pronsole import pronsole
from printrun.utils import format_duration

if __name__ == "__main__" :
	interp = pronsole()
	print "this is a test"
	
	interp.parse_cmdline(sys.argv[1:])
	printing_on = 0
	interp.onecmd("connect")
	time.sleep(5)
	s = socket.socket()        
	host = '130.184.104.40'# ip of raspberry pi 
	print("Socket successfully created")
	port = 12345
	s.bind((host,port))
	print("socket binded")
	#print((c.recv(1024)).decode('utf-8'))
	command = "Ready to receive command"
	while True :
		s.listen(5)
		print("socket is listening")
		c, addr = s.accept()     
		print ('Got connection from', addr)
		#data = input("Enter data to be sent: ")
		#send a thank you message to the client. 
		#c.send(("Thank you for connecting").encode('utf-8'))
		while True:
		   try:
			command = (c.recv(1024)).decode('utf-8')
			print command
			print " Command received. Processing ..."
			
			#control command
			#if(command == "connect"):
				#c.send(("Connecting to printer. Please wait ...").encode('utf-8'))
				#interp.onecmd(command)
				#time.sleep(5)
				#if interp.p.online :
					#c.send(",~#Printer is now online.#~,")
					#c.send("1")
				#else :
					#c.send(",~#Connection failed. Please try again after a while#~,")
					#c.send('0')
			if (command == "disconnect"):
				#c.send(("Disconnecting printer. Please wait ...").encode('utf-8'))
				interp.onecmd(command)
				time.sleep(5)
				if not interp.p.online :
					#c.send(",~#Printer is now offline.#~,")
					c.send("1")
				else :
					#c.send(",~#Cannot disconnect. Please try again after a while#~,")
					c.send("0")
			elif (command == 'probe'):
				c.send("Ultimaker 2,Ultimaker,3D printer,PLA,230,225,205,Square,USB")
			elif (command == 'status'):
				if interp.p.printing:
					c.send("1")
				else:
					c.send("0")
			elif ("load" in command):
				#file = command.split()
				#print file
				#fileName = "/home/pi/MyApp/" + file[1]
				#print fileName
				#f = open('/home/pi/MyApp/current_print.gco','wb')
				f = open('/home/pi/MyApp/current_print.stl','wb')
				c.send('1')#ready to receive
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
				#c.send(interp.message)
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
				#c.send(",~#Printing has been started.#~,")
				c.send("1")
				
	
			elif ("sdprint" in command):#need editing
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
				#c.send(",~#Printing has been started.#~,")
				c.send("1")
				
			
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
				#c.send(",~#Printing has been started.#~,")
				c.send("1")
				
			elif (command == "stop"): 
				interp.onecmd("pause")
				interp.onecmd("off")
				interp.onecmd("home")
				#c.send(",~#Printing has been canceled by user.#~,")
				c.send("1")
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
				c.send('%.1f%%,%s,%s,#' % (progress,interp.status.extruder_temp,interp.status.bed_temp))
			
			elif (command == "gettemp"):
				if (interp.p.online):
					#c.send(",~#Hotend: %s/%s\nBed: %s/%s#~," % (interp.status.extruder_temp, interp.status.extruder_temp_target,interp.status.bed_temp, interp.status.bed_temp_target))
					c.send('%s,%s' % (interp.status.extruder_temp,interp.status.bed_temp))
				else :
					c.send(",~#No printer is connected. Connect to a printer first.#~,")
			
			elif (command == 'close'):
				c.send("Connection terminated!")
				break
			else :
				c.send("Not a valid command!")
			
			if printing_on == 1 and not interp.p.printing:
				printing_on = 0
				interp.onecmd("home")
				time.sleep(1)
				interp.onecmd("settemp 0")
				interp.onecmd("bedtemp 0")
				os.remove('current_print.gco')
		   except socket.error,e:
			s.close()
			s = socket.socket()        
			host = '130.184.104.182'# ip of raspberry pi 
			print("Socket successfully created")
			port = 12345
			s.bind((host,port))
			print("socket binded")
			s.listen(5)
			print("socket is listening")
			c, addr = s.accept()     
			print ('Got connection from', addr)
			
	s.close()
	print "Connection terminated. Thank you."