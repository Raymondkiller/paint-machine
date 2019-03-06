#!/usr/bin/python

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import threading
import serial
import time

dataOld__ = 0
dataNew__ = 0
#socket func
class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        global dataNew__
        self.sendMessage(self.data)
        dataNew__ = self.data
        # print("MESS:", self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    #   self.counter = counter
    def run(self):
        print "Starting " + self.name
        server = SimpleWebSocketServer('', 8000, SimpleEcho)
        server.serveforever()

#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
# ser.port = "/dev/ttyUSB7"
#ser.port = "/dev/ttyS2"
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
# #ser.timeout = None          #block read
# ser.timeout = 1            #non-block read
# #ser.timeout = 2              #timeout block read
# ser.xonxoff = False     #disable software flow control
# ser.rtscts = False     #disable hardware (RTS/CTS) flow control
# ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
# ser.writeTimeout = 2     #timeout for write

# Create new threads: socket thread
thread1 = myThread(1, "socket comunicate")
# thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
# thread2.start()

#main thread: serial run
try: 
    ser.open()
except Exception, e:
    print "error open serial port: " + str(e)
    exit()

if ser.isOpen():

    try:
        # ser.flushInput() #flush input buffer, discarding all its contents
        # ser.flushOutput()#flush output buffer, aborting current output 
        #          #and discard all that is in buffer

        #write data
        # ser.write("start to comunicate!")
        print("write data: start to comunicate!")

    #    time.sleep(0.5)  #give the serial port sometime to receive the data

        ser.writelines("$H\n")
        time.sleep(5)
        ser.writelines("$H\n")
        time.sleep(5)
        ser.writelines("$H\n")
        time.sleep(5)
        ser.writelines("$H\n")
        time.sleep(15)
        ser.writelines("$X\n")
        ser.writelines("G10 L20 X0 Y0\n")
        ser.writelines("G10 L20 Z0\n")
        ser.writelines("G91 G0 Z-75\n")
        time.sleep(4)

        while True:
            if dataNew__ != dataOld__:
                dataOld__ = dataNew__
                DataToSerial = str(dataNew__) + "\n"
                ser.writelines(DataToSerial)
                print(DataToSerial)
            # time.sleep(1)
            # response = ser.readline()
            # print("read data: " + response)
            # ser.close()
    except Exception, e1:
        print "error communicating...: " + str(e1)

else:
    print "cannot open serial port "
