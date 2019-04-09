from threading import Thread
import logging
import sys
import time

class IMU(Thread):
    '''
        This thread polls the IMU board at a constant rate.
        It collects data for the pitch and roll, and writes
        them to shared memory 'imuData' located in launcherProgram.
        It notifies any readers (stickSteering.py) of new IMU data.
    '''
    def __init__(self, inputMonitor, bno):
        Thread.__init__(self)

        self.imuData = inputMonitor["imuData"]
        self.imuReadLock = inputMonitor["imuReadLock"]
        self.imuWriteLock = inputMonitor["imuWriteLock"]
        self.inputMonitor = inputMonitor
        self.event = self.inputMonitor["event"]

        self.bno = bno
        self.pollTime = 0.1

    def run(self):
        #this gets run by the thread
        self.updateIMUData()

    def updateIMUData(self):
        while not self.event.is_set():
            heading, roll, pitch = self.bno.read_euler()
            self.imuWriteLock.acquire(blocking=True, timeout=-1) #wait forever

            self.imuData["pitch"] = pitch
            self.imuData["roll"] = roll

            self.imuReadLock.notify_all()
            self.imuWriteLock.release()
            time.sleep(self.pollTime)

        self.imuWriteLock.acquire(blocking=True, timeout=-1)
        self.imuReadLock.notify_all()
        self.imuWriteLock.release()
        exit()
