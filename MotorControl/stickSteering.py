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

        self.kit = MotorKit()
        self.initMotorKits()
        
        self.motor1 = None
        self.motor2 = None
        self.motor3 = None
        self.motor4 = None
        self.initMotors()

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
        self.actuateMotors()


    def actuateMotors(self):
        while True:
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

            

    def copyIMUInput(self):
        self.pitch = self.imuData["pitch"]
        self.roll = self.imuData["roll"]
        self.heading = self.imuData["heading"]

        #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}', self.heading, self.roll, self.pitch)

    def copyUserInput(self):
        self.D_Up = self.inputMap["D_Up"]
        self.D_Down = self.inputMap["D_Down"]

        self.RX = self.inputMap["RX"]
        self.RY = self.inputMap["RY"]

