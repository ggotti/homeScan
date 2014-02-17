from bluetoothScan import BluetoothScan 
from locationManager import LocationManager
from emailManager import EmailManager
from webSrv import webServer 

import time
from Queue import Queue

def main():
	processingQueue = Queue()
	ble = BluetoothScan(processingQueue)
	email = EmailManager()
	locationMgr = LocationManager(processingQueue,email)

	try:
		while True:
			time.sleep(60)
	except KeyboardInterrupt:
		ble.close()

if __name__ == "__main__":
	print "Welcome to homeScan"
	main()
