"""
author: S M Nahian Al Sunny
company: SE Lab, CSCE, UArk
"""

import sys, time
import traceback
import logging

# Import the serial and printer modules.
#import serial, printer_driver, sys
# Import threading for the condition parameter of printer.
import threading
# Import the list_ports module to enable picking the port through which the printer is connected.
#from serial.tools import list_ports

# @class: printerAdapter
class printerAdapter:
    # @function: init
    def __init__(self,intr, flag):
        # Instance variables.
        self.available = True
        self.axes = {"x":0.0, "y": 0.0, "z":0.0, "a":0.0, "b":0.0}
        self.interp = intr
	self.printing_on = flag
    # end init
    
    # @function: pollDevice
    # @return: Dictionary containing data about the printer.
    # @description: Function required to for this to be an extension of an MTCAdapter.
    def pollDevice(self):
	#interp = pronsole()
        # Structure to hold data.
        printerData = {"availability":"UNAVAILABLE", "xPos":"UNAVAILABLE", "yPos":"UNAVAILABLE","zPos":"UNAVAILABLE",
                       "extruderTemp":"UNAVAILABLE", "extruderTargetTemp":"UNAVAILABLE", "extruderReady":"UNAVAILABLE",
                       "bedTemp":"UNAVAILABLE", "bedTargetTemp":"UNAVAILABLE", "bedReady":"UNAVAILABLE",
                       "buildProgress":"UNAVAILABLE"
                       }
        #print "you have found me!"
        # If the printer was found.
        if self.interp.p.online :
            # Get values from the printer.
            try:
                # ***Make the queries***
             
                # Availability
                if self.interp.p.printing or self.interp.sdprinting or self.printing_on:
			printerData["availability"] = "BUSY"
		else:
			printerData["availability"] = "AVAILABLE"
              
                # Axes
                printerData["xPos"] = self.interp.p.analyzer.abs_x
		printerData["yPos"] = self.interp.p.analyzer.abs_y
		printerData["zPos"] = self.interp.p.analyzer.abs_z
                
                
                # Extruder
                printerData["extruderTemp"] = self.interp.status.extruder_temp
		printerData["extruderTargetTemp"] = self.interp.status.extruder_temp_target
                if self.interp.p.printing  or self.interp.sdprinting or self.printing_on:
                    printerData["extruderReady"] = "BUSY"
                else:
                    printerData["extruderReady"] = "READY"
                
                # bed
                printerData["bedTemp"] = self.interp.status.bed_temp
		printerData["bedTargetTemp"] = self.interp.status.bed_temp_target
                if self.interp.p.printing  or self.interp.sdprinting or self.printing_on:
                    printerData["bedReady"] = "BUSY"
                else:
                    printerData["bedReady"] = "READY"
					
                # Progress
		if self.interp.p.printing:
                    progress = 100 * float(self.interp.p.queueindex) / len(self.interp.p.mainqueue)
		    printerData["buildProgress"] = "%.1f%%" % progress
                elif self.interp.sdprinting:
                    progress = self.interp.percentdone
		    printerData["buildProgress"] = "%.1f%%" % progress
                else:
		    printerData["buildProgress"] = "0.0%"
            except:
                print "printerAdapter.pollprinter, Error getting data from printer "
            # end try-catch
        # end if
        # Otherwise, set things accordingly.
        else:
            self.available = False
        # end else
        
        # Return the reslts.
        return printerData
    # end pollDevice
    
    # @function: setAvailability
    def setAvailability(self, availability):
        self.available = availability
    # end setAvailability
    
    # @function: isAvailable
    def isAvailable(self):
        return self.available
    # end isAvailable
# end printerAdapter

