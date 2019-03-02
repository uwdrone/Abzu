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

    def run(self):
        self.actuateMotors()

    def actuateMotors(self):
        print("This is the actuate motors thread\n")
        #To Do: Include IMU vector into actuation, and calculate a value for
        #for each motor depending on user/imu input "resolveVector" func or something
        #So far, this only does forward/reverse on one motor
        while True:
            self.readLock.acquire(blocking=True, timeout=-1)
            while self.inputMonitor["writers"]>0 or self.inputMonitor["pendingWriters"]>0:
                self.readLock.wait()
            self.inputMonitor["readers"] += 1
            
            print("LY: " + str(self.inputMap["LY"]))
            self.motor5.throttle(self.inputMap["LY"]*1.0,0.08)

            self.inputMonitor["readers"] -= 1
            if self.inputMonitor["pendingWriters"] > 0:
                self.writeLock.notify_all()
            else:
                self.readLock.notify_all()
            self.readLock.release()
            
            time.sleep(0.8)#keeping the delay high for testing for now

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
    
            
