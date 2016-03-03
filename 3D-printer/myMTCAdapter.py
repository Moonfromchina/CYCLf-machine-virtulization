"""
author: S M Nahian Al Sunny
company: SE Lab, CSCE, UArk
"""

import sys

from printerAdapter import *
# For keeping snapshots of the machine states (sequences).
import copy
import traceback

# @class: MTCAdapter
class myMTCAdapter:
    # @function: init
    def __init__(self,adapterType,interp,flag):
        # Initialze adapter as null.
        self.adapter = printerAdapter(interp,flag)
	self.adapterType = adapterType
        # end if printerAdapter
    # end init
    
    # @function: pollDevice
    def pollDevice(self):
        # Return data from the specific adapter's pollDevice function.
        printerData = self.adapter.pollDevice()
	#print printerData
	return printerData
    # end pollDevice
    
# end myMTCAdapter