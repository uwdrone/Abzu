from threading import Thread
import socket
Class PID(Thread):
    def __init__(self, inputMonitor, imuLock=None, imuData=None):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.readLock = inputMonitor["readLock"]
        self.writeLock = inputMonitor["writeLock"]
        self.inputMonitor = inputMonitor

        self.imuLock = imuLock
        self.imuData = imuData

    def P(error):

    def I(error):

    def D(val):

    def convert_cart2cross(angle):
        

### procedure ###
# 1. get angle from IMU
# 2. get controller values
# 3. compute reference angle
# 4. compute D term directly from IMU data
# 5. compute error and transform to motor basis
# 6. compute P and I
# 7. sum P, I, and D; normalise and saturate