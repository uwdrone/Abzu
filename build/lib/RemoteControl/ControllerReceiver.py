from threading import Thread
import time
import socket

class ControllerReceiver(Thread):
    def __init__(self, inputMonitor, socket):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.inputMonitor = inputMonitor
        self.writeLock = inputMonitor["writeLock"]
        self.readLock = inputMonitor["readLock"]
        
        self.HOST = '192.168.1.100' #Server IP
        self.PORT = 12345 #TCP Port
        self.sock = socket

    def run(self):
        self.receiveUserMotorCommands()
    
    def receiveUserMotorCommands(self):
        print("This is the rc command thread\n")
        #managing error exception
        try:
            self.sock.bind((self.HOST, self.PORT))
        except socket.error as e:
            print(e)
            
            return
            
        self.sock.listen(2)
        print("Socket awaiting connections")

        (conn, addr) = self.sock.accept()
        print("Connected")
        
        while True:
            #print("server polling")
            message = conn.recv(256)

            self.writeLock.acquire(blocking=True, timeout=-1)
            self.inputMonitor["pendingWriters"] += 1
            
            while self.inputMonitor["readers"] > 0:
                self.writeLock.wait()     
            self.inputMonitor["writers"] = 1
            
            #print(message.decode())
            self.pushInput(message.decode())

            
            self.inputMonitor["pendingWriters"] -= 1
            self.inputMonitor["writers"] = 0
            self.readLock.notify_all()
            self.writeLock.release()

        #fixes port changing issue
        #Note: This doesn't work if you use ctrlZ to exit the program,
        #so use ctrlC or you will have to change the port #            
        conn.close()            
    
    def pushInput(self, message):
        lst = message.split('|')
        #print("{}".format(lst))
        for item in lst:
            kvp = item.split(':')
            #print("{}".format(kvp))
            try:
                self.inputMap[kvp[0]] = float(kvp[1])
            except:
                return
