from MotorControl.motorThreads import *
from threading import Lock
import signal
import socket

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

inputLock = Lock()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def handler(signum, handler):
    print("signal handler")
    sock.close()
signal.signal(signal.SIGTERM, handler)

def launcher():
    print("Commencing Launcher\n")
    mActr = MotorActuator(inputMap, inputLock)
    mActr.start()
    mCRcvr = MotorCommandsReceiver(inputMap, inputLock, sock)
    mCRcvr.start()

if __name__=='__main__':
    launcher();
