from MotorControl.motorLib import *


def launcher():
    print("Commencing Launcher\n")
    mCRcvr = MotorCommandsReceiver()
    mCRcvr.start()

if __name__=='__main__':
    launcher();
