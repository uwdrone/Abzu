import time

class Motor:
    '''
        Motor wrapper class. Create a motor object by passing in
        the desired adafruit motorkit and the desired motor number.
        The motor will be initialized to initialThrottle. Using a
        wrapper allows for custom throttle behaviour.
    '''
    def __init__(self, motorKit, index, initialThrottle):
        self.motorKit = motorKit
        if index == 1:
            self.motorFunction = motorKit.motor1
        elif index == 2:
            self.motorFunction = motorKit.motor2
        elif index == 3:
            self.motorFunction = motorKit.motor3
        elif index == 4:
            self.motorFunction = motorKit.motor4
        else:
            pass

        self.prevThrottle = initialThrottle

    def throttle(self, value, delay):
        '''
            Throttle the adafruit motor associated with this object
            to the given value.
            Deprecated: Gradually increase/decrease the throttle to
            the given value with the given delay between each step.
        '''
        difference = value - self.prevThrottle
        if difference == 0:
            return
        step = round(difference/(abs(difference)*1), 1)
        temp = self.prevThrottle
        try:
            self.motorFunction.throttle = value
        except:
            self.prevThrottle = value
            return
        self.prevThrottle = value
