import subprocess
import sys
import sh
import re
import Queue
import time
import threading

class BluetoothScan:
    """
    	Class is used to process standard output from hcitool utility.
    	When a line is received, it sends the device MAC and timestamp
    	onto the deviceQueue 
    """   
	def __init__(self,deviceQueue):

		initScript = sh.Command("hciconfig")
		initScript("hci0","reset")
		# Regex pattern to read in MAC addresses
		self.deviceScanRegex = re.compile('(.*:{1,4}.*) (.*)')
		self.closeScanner = False

		self.deviceQueue = deviceQueue
	
		self.scanner = threading.Thread(target=self.bleScanner)
        	self.scanner.setDaemon(True)	
		self.scanner.start()
	
	def close(self):
		self.closeScanner = True
		self.scanner.join()
	
	def hciProcess(self, line, stdin, process):
		"""
			Called every time a new line is read in from the hcitool util
		"""
		line = line.replace('\n', '') 
       		match = self.deviceScanRegex.match(line)
        	if(match != None):
                	#Tuple of the device ID and the scan timestamp
                	deviceTuple = match.group(1), time.time() 

			#Write tuple to queue
			self.deviceQueue.put(deviceTuple)
	
		# If the close flag has been set, terminate
		if self.closeScanner == True:	
			process.terminate()
			return True
 
	def bleScanner(self):
                hcitool=sh.Command("hcitool")
                p = hcitool("lescan",_out=self.hciProcess)
		try:
			p.wait()
		except:	
			print "Unexpected error:", sys.exc_info()[0]	
		print "BleScanner completed"
        
