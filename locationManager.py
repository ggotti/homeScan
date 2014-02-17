import Queue
import time
import threading
import logging


class LocationManager():
    """
        LocationManager is used to maintain a register of devices.
    """

    def __init__(self, deviceQueue, emailManager):
        self.l = logging.getLogger("homeScan")

        self.deviceRegister = {}
        self.deviceQueue = deviceQueue
        self.emailManager = emailManager
        self.on = True
        # Replace with your Fitbit Mac address. Eg, 00:1C:B3:09:85:15
        self.fitbitId = '<YOUREFITBIT-MAC>'

        # Start thread
        self.scanner = threading.Thread(target=self.readQueue)
        self.scanner.setDaemon(True)
        self.scanner.start()

        self.locationThread = threading.Thread(target=self.checkLocation)
        self.locationThread.setDaemon(True)
        self.locationThread.start()

        print "Location Manager Started"

    def readQueue(self):
        while True:
            deviceItem = self.deviceQueue.get(True)

            deviceId = deviceItem[0]
            deviceTime = deviceItem[1]

        #Replace with your fitbit ID
	    if deviceId == self.fitbitId:
            	print deviceItem
            	# Add to map
            	self.deviceRegister[deviceId] = deviceTime

    def checkLocation(self):
        while True:
            self.checkRegister(self.deviceRegister)
            time.sleep(10)

    def checkRegister(self, deviceRegister):
        overTimeCounter = 0
        currentTime = time.time()
        for devItem in deviceRegister:
            # Check timestamp
            deviceTime = deviceRegister[devItem]
            if deviceTime < (currentTime - (60 * 30)):
                overTimeCounter += 1
            # print deviceTime

        print deviceRegister
        # If no device has been found for 30 minutes, and self.on is set to True,
        # send deviceOff email
        if len(deviceRegister) != 0 and len(deviceRegister) == overTimeCounter and self.on == True:
            self.on = False
            print "Switch off"
            self.emailManager.sendMsg("#deviceOff","No devices found")
        # If a device is found, and self.on is set to False, send deviceOn email
        elif overTimeCounter < len(deviceRegister) and self.on == False:
            self.on = True
            print "Switch on"
            self.emailManager.sendMsg("#deviceOn","Device found")

    def getDeviceRegister(self):
        return self.deviceRegister
