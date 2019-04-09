from threading import Thread
import time
import socket

class ControllerReceiver(Thread):
    '''
        A server that waits for incoming user input over a TCP port
        User input is copied into shared memory 'inputMap' under the
        protection of read-write lock. Readers are notified whenever
        there is new user input.
    '''
    def __init__(self, inputMonitor, socket):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.inputMonitor = inputMonitor
        self.writeLock = inputMonitor["writeLock"]
        self.readLock = inputMonitor["readLock"]
        self.event = inputMonitor["event"]

        self.HOST = '192.168.1.102' #Server IP
        self.PORT = 12345 #TCP Port
        self.sock = socket #TCP socket

        self.square = False
        self.startTime = None

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

        while not self.event.is_set():
            message = conn.recv(256)

            self.writeLock.acquire(blocking=True, timeout=-1)
            self.inputMonitor["pendingWriters"] += 1

            while self.inputMonitor["readers"] > 0:
                self.writeLock.wait()
            self.inputMonitor["writers"] = 1

            self.pushInput(message.decode())
            self.shutdownCheck()

            self.inputMonitor["pendingWriters"] -= 1
            self.inputMonitor["writers"] = 0
            self.readLock.notify_all()
            self.writeLock.release()

        #Note: This doesn't work if you use ctrlZ to exit the program,
        #so use ctrlC or you will have to change the port #
        conn.close()
        self.readLock.acquire(blocking=True, timeout=-1)
        self.readLock.notify_all()
        self.readLock.release()
        exit()

    def pushInput(self, message):
        '''
            Copy inputMap into shared memory
        '''
        lst = message.split('|')
        for item in lst:
            kvp = item.split(':')
            try:
                self.inputMap[kvp[0]] = float(kvp[1])
            except:
                return

    def shutdownCheck(self):
        '''
            Sets the event after square has been held down for at least
            5 seconds. Each thread (including this one) loops on the condition
            that the event is not set. Thus setting the event will shutdown the
            software system entirely.
        '''
        print(self.square)
        if self.square == False and self.inputMap["square"] == 1:
            self.startTime = time.time()
            self.square = True
        elif self.square == True and self.inputMap["square"] == 0:
            elapsedTime = time.time() - self.startTime
            print(elapsedTime)
            if elapsedTime > 5:
                print("kill signal")
                self.event.set()
            else:
                self.square = False
