from threading import Thread
from .motor import Motor
from adafruit_motorkit import MotorKit
import time
import socket

class MotorCommandsReceiver(Thread):
    def __init__(self, inputMap, inputLock, socket):
        Thread.__init__(self)
        self.inputMap = inputMap
        self.inputLock = inputLock
        self.HOST = '192.168.1.101' #Server IP
        self.PORT = 12349 #TCP Port
        self.sock = socket

    def run(self):
        self.receiveUserMotorCommands()
    
    def receiveUserMotorCommands(self):
        print("This is the motor command thread\n")
        #managing error exception
        try:
            self.sock.bind((self.HOST, self.PORT))
        except socket.error:
            print("bind failed")
            self.sock.close()
            
        self.sock.listen(2)
        print("Socket awaiting connections")

        (conn, addr) = self.sock.accept()
        print("Connected")
        
        while True:
            message = conn.recv(4096)
            
            if self.inputLock.acquire(blocking=False)==True:
                #print("pushing commands")
                self.pushInput(message.decode())
                self.inputLock.release()
    
    def pushInput(self, message):
        lst = message.split('|')
        #print("{}".format(lst))
        for item in lst:
            kvp = item.split(':')
            #print("{}".format(kvp))
            self.inputMap[kvp[0]] = float(kvp[1])
            

class MotorActuator(Thread):
    def __init__(self, inputMap, inputLock, imuLock=None, imuData=None):
        Thread.__init__(self)
        self.inputMap = inputMap
        self.inputLock = inputLock
        
        self.imuLock = imuLock
        self.imuData = imuData
        
        self.kit = MotorKit()
        self.kit1 = MotorKit(0x61)
        self.initMotorKits(self.kit, self.kit1)
        self.kit1.motor1.throttle = 0.0
        self.initMotors()

    def run(self):
        self.actuateMotors()

    def actuateMotors(self):
        print("This is the actuate motors thread\n")
        #To Do: Include IMU vector into actuation, and calculate a value for
        #for each motor depending on user/imu input "resolveVector" func or something
        #So far, this only does forward/reverse on one motor
        while True:
            self.inputLock.acquire(blocking=True, timeout=-1)
            print("LY: " + str(self.inputMap["LY"]))
            self.motor5.throttle(self.inputMap["LY"]*1.0,0.08)
                
            self.inputLock.release()
            time.sleep(0.8)#keeping the delay high for testing for now

    def initMotors(self):
        self.motor1 = Motor(self.kit, 1, 0.0) #attitude 1
        self.motor2 = Motor(self.kit, 2, 0.0) #attitude 2
        self.motor3 = Motor(self.kit, 3, 0.0) #attitude 3 
        self.motor4 = Motor(self.kit, 4, 0.0) #attitude 3

        self.motor5 = Motor(self.kit1, 1, 0.0) #forward thrust 1
        self.motor6 = Motor(self.kit1, 2, 0.0) #forward thrust 2

    def initMotorKits(self, *args):
        for kit in args:
            kit.motor1.throttle = 0.0
            kit.motor2.throttle = 0.0
            kit.motor3.throttle = 0.0
            kit.motor4.throttle = 0.0
    
            
