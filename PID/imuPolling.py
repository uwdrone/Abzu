from threading import Thread
import logging
import sys
import time

#from Adafruit_BNO055 import BNO055

class IMU(Thread):
    def __init__(self, inputMonitor, bno):
        Thread.__init__(self)
        
        self.imuData = inputMonitor["imuData"]
        self.imuReadLock = inputMonitor["imuReadLock"]
        self.imuWriteLock = inputMonitor["imuWriteLock"]

        self.inputMonitor = inputMonitor
        self.event = self.inputMonitor["event"]

        self.bno = bno
        
    def run(self):
        #this gets run by the thread
        self.updateIMUData()

    def updateIMUData(self):
        while not self.event.is_set():
            heading, roll, pitch = self.bno.read_euler()
            #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}', heading, roll, pitch)

            self.imuWriteLock.acquire(blocking=True, timeout=-1)
            self.imuData["pitch"] = pitch
            self.imuData["roll"] = roll
            self.imuReadLock.notify_all()
            self.imuWriteLock.release()

            time.sleep(0.1)
        self.imuWriteLock.acquire(blocking=True, timeout=-1)
        self.imuReadLock.notify_all()
        self.imuWriteLock.release()
        exit()
