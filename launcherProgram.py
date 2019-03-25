from MotorControl.motorThreads import *
from RemoteControl.ControllerReceiver import *
from CameraControl.Record import *
from MotorControl.skidSteering import *
from MotorControl.stickSteering import *
from CameraControl.templateFiles.videoStreamThread import *
from Adafruit_BNO055 import BNO055
from PID.imuPolling import *
from threading import Lock
from threading import Condition
import signal
import socket
import time

inputMap = {
        "LX": 0.0,
        "LY": 0.0,
        "RX": 0.0,
        "RY": 0.0,
        "x_button": 0.0,
        "circle": 0.0,
        "triangle": 0.0,
        "square": 0.0,
        "L1": 0.0,
        "R1": 0.0,
        "L2": 0.0,
        "R2": 0.0,
        "Select": 0.0,
        "Start": 0.0,
        "PS_Button": 0.0,
        "L3": 0.0,
        "R3": 0.0,
        "D_Up": 0.0,
        "D_Down": 0.0,
        "D_Left": 0.0,
        "D_Right": 0.0
    }

imuData = {
        "pitch": 0.0,
        "roll": 0.0,
        "heading": 0.0
    }


inputMutex = Lock()
readers = 0
pendingWriters = 0
writers = 0
readLock = Condition(inputMutex)
writeLock = Condition(inputMutex)

imuMutex = Lock()
imuReadLock = Condition(imuMutex)
imuWriteLock = Condition(imuMutex)

inputMonitor = {
    "inputMutex": inputMutex,
    "readers": 0,
    "writers": 0,
    "pendingWriters": 0,
    "pendingReaders": 0,
    "inputMap": inputMap,
    "readLock": readLock,
    "writeLock": writeLock,
    "imuMutex": imuMutex,
    "imuReadLock": imuReadLock,
    "imuWriteLock": imuWriteLock,
    "imuData": imuData
    }



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

##bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
##if not bno.begin():
##    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')


def handler(signum, handler):
    print("signal handler")
    sock.close()
signal.signal(signal.SIGTERM, handler)

def launcher():
    print("Commencing Launcher\n")
    rcRcvr = ControllerReceiver(inputMonitor, sock)
    rcRcvr.start()

    #imuPoll = IMU(inputMonitor, bno)
    #imuPoll.start()
    
##    mActr = MotorActuator(inputMonitor)
##    mActr.start()
    skidSteer = SkidSteering(inputMonitor)
    skidSteer.start()

    stickSteer = StickSteering(inputMonitor)
    stickSteer.start()
    
    #camCorder = VideoRecorder(inputMonitor)
    #camCorder.start()
    videoStream = StreamThread()
    videoStream.start()
    
if __name__=='__main__':
    launcher();
