from threading import Thread
from .motor import Motor
from adafruit_motorkit import MotorKit
from .pid import *
import time
import socket
import math

class StickSteering(Thread):
    def __init__(self, inputMonitor):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.readLock = inputMonitor["readLock"]
        self.writeLock = inputMonitor["writeLock"]
        self.inputMonitor = inputMonitor
        self.event = inputMonitor["event"]

        self.RX = 0.0
        self.RY = 0.0

        self.pitch = 0.0
        self.roll = 0.0
        self.heading = 0.0

        self.D_Up = 0
        self.D_Down = 0

        self.imuReadLock = inputMonitor["imuReadLock"]
        self.imuWriteLock = inputMonitor["imuWriteLock"]
        self.imuData = inputMonitor["imuData"]

        self.kit = MotorKit(0x61)
        self.initMotorKits()
        
        self.motor1 = None
        self.motor2 = None
        self.motor3 = None
        self.motor4 = None
        self.initMotors()

        self.pid = PID()
        self.cross1 = 0.0
        self.cross2 = 0.0

        self.motor1Throttle = 0.0
        self.motor2Throttle = 0.0
        self.motor3Throttle = 0.0
        self.motor4Throttle = 0.0

    def initMotorKits(self):
        self.kit.motor1.throttle = 0.0
        self.kit.motor2.throttle = 0.0
        self.kit.motor3.throttle = 0.0
        self.kit.motor4.throttle = 0.0

    def initMotors(self):
        self.motor1 = Motor(self.kit, 1, 0.0)
        self.motor2 = Motor(self.kit, 2, 0.0)
        self.motor3 = Motor(self.kit, 3, 0.0)
        self.motor4 = Motor(self.kit, 4, 0.0)

    def run(self):
        while not self.event.is_set():
            self.imuReadLock.acquire(blocking=True, timeout=-1)
            self.imuReadLock.wait()

            self.copyIMUInput()

            #self.imuWriteLock.notify_all()
            self.imuReadLock.release()

            self.readLock.acquire(blocking=True, timeout=-1)
            self.inputMonitor["readers"] += 1

            self.copyUserInput()

            self.inputMonitor["readers"] -= 1
            if self.inputMonitor["pendingWriters"] > 0:
                self.writeLock.notify_all()
            elif self.inputMonitor["pendingReaders"]>0 or self.inputMonitor["readers"]>0:
                self.readLock.notify_all()
            else:
                pass
            self.readLock.release()

            self.stick()


    def actuateMotors(self):
        self.motor1.throttle(self.motor1Throttle, 0.01)
        self.motor2.throttle(self.motor2Throttle, 0.01)
        self.motor3.throttle(self.motor3Throttle, 0.01)
        self.motor4.throttle(self.motor4Throttle, 0.01)

            
    def stick(self):
        pitchJS = -1.0*self.RY*math.pi/3
        rollJS = self.RX*math.pi/3

        print("RX: " + str(self.RX))
        print("RY: " + str(self.RY))

        pitchIMU = math.radians(self.pitch)
        rollIMU = math.radians(self.roll)
        if self.pitch < 4.5 and self.pitch > -4.5:
            pitchIMU = 0.0
        if self.roll < 4.5 and self.roll > -4.5:
            rollIMU = 0.0

        angle = (pitchIMU, rollIMU)
        ref = (pitchJS, rollJS)

        cross1, cross2 = self.pid.updatePID(angle, ref)
        self.cross1 = cross1
        self.cross2 = cross2
        print("Cross1={} Cross2={}".format(round(cross1,1), round(cross2,1)))

        self.motor1Throttle = self.cross1
        self.motor3Throttle = -1.0*self.cross1

        self.motor2Throttle = self.cross2
        self.motor4Throttle = -1.0*self.cross2

        self.depth()
        self.actuateMotors()
        

    def copyIMUInput(self):
        self.pitch = self.imuData["pitch"]
        self.roll = self.imuData["roll"]
        self.heading = self.imuData["heading"]

        print('Heading={} Roll={} Pitch={}'.format(self.heading, self.roll, self.pitch))

    def copyUserInput(self):
        self.D_Up = self.inputMap["D_Up"]
        self.D_Down = self.inputMap["D_Down"]
        
        self.RX = self.inputMap["RX"]
        self.RY = self.inputMap["RY"]

##        print("RX: " + str(self.RX))
##        print("RY: " + str(self.RY))

    def depth(self):
        if self.D_Up == 1.0:
            self.ascend()
        elif self.D_Down == 1.0:
            self.descend()
        else:
            pass

    def ascend(self):
        diff1 = 1.0 - abs(self.cross1)
        diff2 = 1.0 - abs(self.cross2)

        self.motor1Throttle = self.cross1 - diff1
        self.motor3Throttle = -1.0*self.cross1 - diff1

        self.motor2Throttle = self.cross2 - diff2
        self.motor4Throttle = -1.0*self.cross2 - diff2

    def descend(self):
        diff1 = 1.0 - abs(self.cross1)
        diff2 = 1.0 - abs(self.cross2)

        self.motor1Throttle = self.cross1 + diff1
        self.motor3Throttle = -1.0*self.cross1 + diff1

        self.motor2Throttle = self.cross2 + diff2
        self.motor4Throttle = -1.0*self.cross2 + diff2
