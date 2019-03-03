from threading import Thread
from .motor import Motor
from adafruit_motorkit import MotorKit
import time
import socket            

class MotorActuator(Thread):
    def __init__(self, inputMonitor, imuLock=None, imuData=None):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.readLock = inputMonitor["readLock"]
        self.writeLock = inputMonitor["writeLock"]
        self.inputMonitor = inputMonitor
        
        self.imuLock = imuLock
        self.imuData = imuData
        
        self.kit = MotorKit()
        self.kit1 = MotorKit(0x61)
        self.initMotorKits()

        self.motor1 = None
        self.motor2 = None
        self.motor3 = None
        self.motor4 = None
        self.motor5 = None
        self.motor6 = None
        self.initMotors()

    def initMotors(self):
        self.motor1 = Motor(self.kit, 1, 0.0) #attitude 1
        self.motor2 = Motor(self.kit, 2, 0.0) #attitude 2
        self.motor3 = Motor(self.kit, 3, 0.0) #attitude 3 
        self.motor4 = Motor(self.kit, 4, 0.0) #attitude 3

        self.motor5 = Motor(self.kit1, 1, 0.0) #forward thrust 1
        self.motor6 = Motor(self.kit1, 2, 0.0) #forward thrust 2

    def initMotorKits(self):
        self.kit.motor1.throttle = 0.0
        self.kit.motor2.throttle = 0.0
        self.kit.motor3.throttle = 0.0
        self.kit.motor4.throttle = 0.0

        
        self.kit1.motor1.throttle = 0.0
        self.kit1.motor2.throttle = 0.0

    def run(self):
        self.actuateMotors()

    def actuateMotors(self):
        print("This is the actuate motors thread\n")
        #To Do: Include IMU vector into actuation, and calculate a value for
        #for each motor depending on user/imu input "resolveVector" func or something
        
        while True:
            self.readLock.acquire(blocking=True, timeout=-1)
            self.inputMonitor["pendingReaders"] += 1
            self.readLock.wait()
            
            self.inputMonitor["pendingReaders"] -= 1
            self.inputMonitor["readers"] += 1
            
            self.depth()
            self.skid()

            self.inputMonitor["readers"] -= 1
            if self.inputMonitor["pendingWriters"] > 0:
                self.writeLock.notify_all()
            if self.inputMonitor["pendingReaders"]>0 or self.inputMonitor["readers"]>0:
                self.readLock.notify_all()
            self.readLock.release()
            

    def skid(self):
        pass

    def depth(self):
        if self.inputMap["D_Up"] == 1.0:
            self.ascend()
        elif self.inputMap["D_Down"] == 1.0:
            self.descend()
        else:
            #this section will change when we get IMU vector
            self.motor1.throttle(0.0, 0.01)
            self.motor2.throttle(0.0, 0.01)
            self.motor3.throttle(0.0, 0.01)
            self.motor5.throttle(0.0, 0.01)

    def ascend(self):
        self.motor1.throttle(1.0, 0.01)
        self.motor2.throttle(1.0, 0.01)
        self.motor3.throttle(1.0, 0.01)
        self.motor5.throttle(1.0, 0.01)

    def descend(self):
        self.motor1.throttle(-1.0, 0.01)
        self.motor2.throttle(-1.0, 0.01)
        self.motor3.throttle(-1.0, 0.01)
        self.motor5.throttle(-1.0, 0.01)
    
            
