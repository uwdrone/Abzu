from threading import Thread
from .motor import Motor
from adafruit_motorkit import MotorKit
import time
import socket
import math

class MotorActuator(Thread):
    def __init__(self, inputMonitor, imuLock=None, imuData=None):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.readLock = inputMonitor["readLock"]
        self.writeLock = inputMonitor["writeLock"]
        self.inputMonitor = inputMonitor

        self.localInputMap = dict()
        
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

            self.copyInput()

            self.inputMonitor["readers"] -= 1
            if self.inputMonitor["pendingWriters"] > 0:
                self.writeLock.notify_all()
            elif self.inputMonitor["pendingReaders"]>0 or self.inputMonitor["readers"]>0:
                self.readLock.notify_all()
            else:
                pass
            self.readLock.release()

            #actuate
            #self.depth()
            self.skid()
            

    def skid(self):
        LX = self.inputMap["LX"]
        LY = -1*self.inputMap["LY"]
        #print("LX: " + str(LX))
        #print("LY: " + str(LY))

        theta = float()
        
        if LX == 0.0 and LY == 0.0:
            print("Throttle off")
            self.motor5.throttle(0.0, 0.01)
            self.motor6.throttle(0.0, 0.01)
            return
        
        elif LX == 0.0:
            if LY > 0.0:
                theta = math.radians(90.0)
            if LY < 0.0:
                theta = math.radians(270.0)
            
            H = abs(LY/math.sin(theta))
            
        elif LY == 0.0:
            if LX > 0.0:
                theta = math.radians(0.0)
            if LX < 0.0:
                theta = math.radians(180.0)

            H = abs(LX/math.cos(theta))
            
        else:
            theta = math.atan(abs(LY/LX))
            H = abs(LX/math.cos(theta))

        h = H - 1
        if h <= 0.0:
            x = LX
            y = LY 
        else:
            if LX < 0.0:
                x = -1.0*(abs(LX) - h*math.cos(theta))
            else:
                x = LX - h*math.cos(theta)
            if LY < 0.0:
                y = -1.0*(abs(LY) - h*math.sin(theta))
            else:
                y = LY - h*math.sin(theta)
        
        #print("Theta: " + str(math.degrees(theta)))
        #print("X: " + str(x))
        #print("Y: " + str(y))

        magnitude = round(math.sqrt(y*y + x*x), 1)
        #print("Magnitude: " + str(magnitude))
        if x > 0.0:
            #Right two quadrants
            self.motor5.throttle(round(y*(1-x), 1), 0.01)
            if y > 0.0:
                self.motor6.throttle(magnitude, 0.01)
                print("Up-Right")
                print("Motor1: " + str(magnitude))
                print("Motor2: " + str(round(y*(1-x), 1)))
            elif y < 0.0:
                self.motor6.throttle(-1.0*magnitude, 0.01)
                print("Down-Right")
                print("Motor1: " + str(magnitude))
                print("Motor2: " + str(round(y*(1-x), 1)))
            else:
                self.motor5.throttle(0.0, 0.01)
                self.motor6.throttle(magnitude, 0.01)
                print("Right")
                print("Motor1: " + str(magnitude))
        elif x < 0.0:
            #Left two quadrants
            self.motor6.throttle(round(y*abs(-1-x), 1), 0.01)
            if y > 0.0:
                self.motor5.throttle(magnitude, 0.01)
                print("Up-Left")
                print("Motor1: " + str(round(y*abs(-1-x), 1)))
                print("Motor2: " + str(magnitude))
            elif y < 0.0:
                self.motor5.throttle(-1.0*magnitude, 0.01)
                print("Down-Left")
                print("Motor1: " + str(round(y*abs(-1-x), 1)))
                print("Motor2: " + str(-1.0*magnitude))
            else:
                self.motor6.throttle(0.0, 0.01)
                self.motor5.throttle(magnitude, 0.01)
                print("Left")
                print("Motor2: " + str(magnitude))
        else:
            print("Straight")
            self.motor6.throttle(round(y, 1), 0.01)
            self.motor5.throttle(round(y, 1), 0.01)
        
        

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
            self.motor4.throttle(0.0, 0.01)

    def ascend(self):
        self.motor1.throttle(1.0, 0.01)
        self.motor2.throttle(1.0, 0.01)
        self.motor3.throttle(1.0, 0.01)
        self.motor4.throttle(1.0, 0.01)

    def descend(self):
        self.motor1.throttle(-1.0, 0.01)
        self.motor2.throttle(-1.0, 0.01)
        self.motor3.throttle(-1.0, 0.01)
        self.motor4.throttle(-1.0, 0.01)

    def copyInput(self):
        for key, value in self.inputMap.items():
            self.localInputMap[key] = value
    
    
            
