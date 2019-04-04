from threading import Thread
from .motor import Motor
from adafruit_motorkit import MotorKit
import time
import socket
import math

class SkidSteering(Thread):
    def __init__(self, inputMonitor):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.readLock = inputMonitor["readLock"]
        self.writeLock = inputMonitor["writeLock"]
        self.inputMonitor = inputMonitor

        self.LX = 0.0
        self.LY = 0.0
        
        self.kit = MotorKit(0x61)
        self.initMotorKits()

        self.motorLeft = None
        self.motorRight = None
        
        self.initMotors()

    def initMotorKits(self):
        self.kit.motor1.throttle = 0.0
        self.kit.motor2.throttle = 0.0
        self.kit.motor3.throttle = 0.0
        self.kit.motor4.throttle = 0.0

    def initMotors(self):
        self.motorLeft = Motor(self.kit, 1, 0.0)
        self.motorRight = Motor(self.kit, 2, 0.0)

    def run(self):
        self.actuateMotors()

    def actuateMotors(self):
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
            self.skid()

    def skid(self):
        LX = self.LX
        LY = -1*self.LY
        #print("LX: " + str(LX))
        #print("LY: " + str(LY))

        theta = float()
        
        if LX == 0.0 and LY == 0.0:
            #print("Throttle off")
            self.motorLeft.throttle(0.0, 0.01)
            self.motorRight.throttle(0.0, 0.01)
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
            self.motorRight.throttle(round(y*(1-x), 1), 0.01)
            if y > 0.0:
                self.motorLeft.throttle(magnitude, 0.01)
                print("Up-Right")
                print("Motor1: " + str(magnitude))
                print("Motor2: " + str(round(y*(1-x), 1)))
            elif y < 0.0:
                self.motorLeft.throttle(-1.0*magnitude, 0.01)
                print("Down-Right")
                print("Motor1: " + str(magnitude))
                print("Motor2: " + str(round(y*(1-x), 1)))
            else:
                self.motorRight.throttle(0.0, 0.01)
                self.motorLeft.throttle(magnitude, 0.01)
                print("Right")
                print("Motor1: " + str(magnitude))
        elif x < 0.0:
            #Left two quadrants
            self.motorLeft.throttle(round(y*abs(-1-x), 1), 0.01)
            if y > 0.0:
                self.motorRight.throttle(magnitude, 0.01)
                print("Up-Left")
                print("Motor1: " + str(round(y*abs(-1-x), 1)))
                print("Motor2: " + str(magnitude))
            elif y < 0.0:
                self.motorRight.throttle(-1.0*magnitude, 0.01)
                print("Down-Left")
                print("Motor1: " + str(round(y*abs(-1-x), 1)))
                print("Motor2: " + str(-1.0*magnitude))
            else:
                self.motorLeft.throttle(0.0, 0.01)
                self.motorRight.throttle(magnitude, 0.01)
                print("Left")
                print("Motor2: " + str(magnitude))
        else:
            print("Straight")
            self.motorLeft.throttle(round(y, 1), 0.01)
            self.motorRight.throttle(round(y, 1), 0.01)
        
    
    def copyInput(self):
        self.LX = self.inputMap["LX"]
        self.LY = self.inputMap["LY"]

















        
