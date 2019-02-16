from MotorControl.motorThreads import *
from threading import Lock

inputMap = {
        "LX": 0,
        "LY": 0,
        "RX": 0,
        "RY": 0,
        "x_button": 0,
        "circle": 0,
        "triangle": 0,
        "square": 0,
        "L1": 0,
        "R1": 0,
        "L2": 0,
        "R2": 0,
        "Select": 0,
        "Start": 0,
        "PS_Button": 0,
        "L3": 0,
        "R3": 0,
        "D_Up": 0,
        "D_Down": 0,
        "D_Left": 0,
        "D_Right": 0
    }

inputLock = Lock()

def launcher():
    print("Commencing Launcher\n")
    mActr = MotorActuator(inputMap, inputLock)
    mActr.start()
    mCRcvr = MotorCommandsReceiver(inputMap, inputLock)
    mCRcvr.start()

if __name__=='__main__':
    launcher();
