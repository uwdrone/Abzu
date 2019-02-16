from threading import Thread
from .motor import Motor
from adafruit_motorkit import MotorKit
import time

class MotorCommandsReceiver(Thread):
    def __init__(self, inputMap, inputLock):
        Thread.__init__(self)
        self.inputMap = inputMap
        self.inputLock = inputLock

    def run(self):
        self.receiveUserMotorCommands()
    
    def receiveUserMotorCommands(self):
        while(self.inputLock.acquire(blocking=False)!=True):
            print("This is the motor command thread\n")
        self.inputMap["LY"] = 0
        self.inputLock.release()

class MotorActuator(Thread):
    def __init__(self, inputMap, inputLock, imuLock=None, imuData=None):
        Thread.__init__(self)
        self.inputMap = inputMap
        self.inputLock = inputLock
        
        self.imuLock = imuLock
        self.imuData = imuData
        
        self.kit = MotorKit()
        self.kit1 = MotorKit(0x61)
        #self.initMotorKits(self.kit, self.kit1)
        self.kit1.motor1.throttle = 0.0
        self.initMotors()

    def run(self):
        self.actuateMotors()

    def actuateMotors(self):
        print("This is the actuate motors thread\n")
        while True:
            self.inputLock.acquire(timeout=-1)
            if self.inputMap["LY"] == 1:
                self.motor5.throttle(1.0,0.05)
            elif self.inputMap["LY"] == 0:
                self.motor5.throttle(0.0,0.05)
                
            self.inputLock.release()
            time.sleep(1)

    def initMotors(self):
        self.motor1 = Motor(self.kit, 1, 0.0) #attitude 1
        self.motor2 = Motor(self.kit, 2, 0.0) #attitude 2
        self.motor3 = Motor(self.kit, 3, 0.0) #attitude 3 
        self.motor4 = Motor(self.kit, 4, 0.0) #attitude 3

        self.motor5 = Motor(self.kit1, 1, 0.0) #forward thrust 1
        self.motor6 = Motor(self.kit1, 2, 0.0) #forward thrust 2

    
