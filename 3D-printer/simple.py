import os,sys
import traceback
import logging
import time
import socket
import pickle

from printrun.pronsole import pronsole
from printrun.utils import format_duration
from MTCAdapter import *
import adapter_test2


if __name__ == "__main__" :
	
	print "this is a test"
	#time.sleep(5)
	command = ""
	while True :
		command = raw_input("Enter command here: ")
		if(command == "poll"):
			fp = open("tempData.pkl")
			data = pickle.load(fp)
			print data	   
			
