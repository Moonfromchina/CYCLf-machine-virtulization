"""
author: S M Nahian Al Sunny
company: SE Lab, CSCE, UArk
"""

import sys
import pickle

from printerAdapter import *
# For keeping snapshots of the machine states (sequences).
import copy
import traceback

# @class: MTCAdapter
class MTCAdapter:
    # @function: init
    def __init__(self,adapterType,interp):
        # Initialze adapter as null.
        #self.adapter = printerAdapter(interp)
	self.adapterType = adapterType
        # end if printerAdapter
    # end init
    
    # @function: pollDevice
    def pollDevice(self):
        # Return data from the specific adapter's pollDevice function.
        #fp = open("tempData.pkl","rb")
	#data = pickle.load(fp)
	try:
		with open("tempData.pkl","rb") as fp:
			data = pickle.load(fp)
	except :
		with open("tempData2.pkl","rb") as fp:
			data = pickle.load(fp)
	print data
	with open("tempData2.pkl","wb") as fs:
		pickle.dump(data,fs)
	#print printerData
	return data
    # end pollDevice
    
# end MTCAdapter


