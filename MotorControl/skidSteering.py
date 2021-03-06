from threading import Thread
from .motor import Motor
from adafruit_motorkit import MotorKit
import time
import socket
import math

class SkidSteering(Thread):
    '''
        This thread controls the rear motors on the drone.
    '''
    def __init__(self, inputMonitor):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.readLock = inputMonitor["readLock"]
        self.writeLock = inputMonitor["writeLock"]
        self.inputMonitor = inputMonitor
        self.event = inputMonitor["event"]

        self.LX = 0.0
        self.LY = 0.0
        self.delay = 0.01

        #0x61 is address of second motor hat
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
        while not self.event.is_set():
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
        exit()

    def skid(self):
        LX = self.LX
        LY = -1*self.LY
        theta = float()

        if LX == 0.0 and LY == 0.0:
            self.motorLeft.throttle(0.0, self.delay)
            self.motorRight.throttle(0.0, self.delay)
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

        magnitude = round(math.sqrt(y*y + x*x), 1)
        if x > 0.0:
            #Right two quadrants
            self.motorRight.throttle(-1.0*round(y*(1-x), 1), self.delay)
            if y > 0.0:
                self.motorLeft.throttle(magnitude, self.delay)
                print("Up-Right")
                print("MotorLeft: " + str(magnitude))
                print("MotorRight: " + str(-1.0*round(y*(1-x), 1)))
            elif y < 0.0:
                self.motorLeft.throttle(-1.0*magnitude, self.delay)
                print("Down-Right")
                print("MotorLeft: " + str(magnitude))
                print("MotorRight: " + str(-1.0*round(y*(1-x), 1)))
            else:
                self.motorRight.throttle(0.0, self.delay)
                self.motorLeft.throttle(magnitude, self.delay)
                print("Right")
                print("MotorLeft: " + str(magnitude))
        elif x < 0.0:
            #Left two quadrants
            self.motorLeft.throttle(round(y*abs(-1-x), 1), self.delay)
            if y > 0.0:
                self.motorRight.throttle(-1.0*magnitude, self.delay)
                print("Up-Left")
                print("MotorLeft: " + str(round(y*abs(-1-x), 1)))
                print("MotorRight: " + str(-1.0*magnitude))
            elif y < 0.0:
                self.motorRight.throttle(magnitude, self.delay)
                print("Down-Left")
                print("MotorLeft: " + str(round(y*abs(-1-x), 1)))
                print("MotorRight: " + str(magnitude))
            else:
                self.motorLeft.throttle(0.0, self.delay)
                self.motorRight.throttle(-1.0*magnitude, self.delay)
                print("Left")
                print("MotorRight: " + str(-1.0*magnitude))
        else:
            print("Straight")
            self.motorLeft.throttle(round(y, 1), self.delay)
            self.motorRight.throttle(-1.0*round(y, 1), self.delay)

    def copyInput(self):
        self.LX = self.inputMap["LX"]
        self.LY = self.inputMap["LY"]
