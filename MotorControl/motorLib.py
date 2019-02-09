from threading import Thread

class MotorCommandsReceiver(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.receiveUserMotorCommands()
    
    def receiveUserMotorCommands(self):
        print("This is the motor command thread\n")


class MotorActuator(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.actuateMotors()

    def actuateMotors():
        print("This is the actuate motors thread\n")

class IMUReceiver(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.receiveIMUVector()
        
    def receiveIMUVector():
        pass
