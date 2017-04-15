import serial, time, sys

rfid_reader = "/dev/tty.usbserial-AL037J8X"
ser = serial.Serial(rfid_reader, timeout=1)
print("Connected to RFID reader on:", rfid_reader)

def read_rfid():
	# try:
	    # while True:                                         # loop forever until a tag is read
	ser.flushInput()                                # flush any extra data from the serial port
	rfid_data = ser.readline().strip()              # read the rfid data
                        
	if len(rfid_data) > 0:                          # check for incoming card data
		rfid_data = rfid_data[1:11]                 # strip off all data but the tag number
		print("Card Scanned. Tag ID:", rfid_data)    # print the tag number
		print("Type of id: ", type(rfid_data))
		return rfid_data
	return None
	        
	# except KeyboardInterrupt:                               # if ctrl-c'd , cleanup your mess and exit
	#     print("Caught interrupt, exiting...")
	                              
	# except:
	#     print("Unexpected error:", sys.exc_info()[0])
	#     raise

	# finally:
	#     ser.close()
	#     print("Closing serial port")
	#     return None